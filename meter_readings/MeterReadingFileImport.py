import datetime
import math

import pandas
from django.core.management import CommandError
from django.db import IntegrityError
from pandas import DataFrame

from meter_readings.models import MeterReading, RegisterReading

HANDLED_DATA_TYPE_CODES = ["026", "027", "028", "029", "030", "032", "033"]


class MeterReadingFileImport:
    """
    Class to handle file imports
    """

    def __init__(self, file_location: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.file_location = file_location

    def __read_file_to_data_frame(self) -> DataFrame:
        # Open and then read the file into a data frame
        with open(self.file_location, "r", encoding="utf8") as meter_readings_file:
            return pandas.read_csv(meter_readings_file, header=None, delimiter="|")

    @staticmethod
    def __validate_row(row):
        # The first column in the row tells us the type of data. Make sure it's in one of the handled types.
        if row[0] not in HANDLED_DATA_TYPE_CODES:
            # Abort everything even if some might have been fine. We now don't trust the data.
            raise CommandError(f'Unhandled data type in file: {row[0]}.')

    def import_data_to_database(self):
        # Read data to data frame
        readings_data_frame = self.__read_file_to_data_frame()

        # Get the final row number for validation later
        final_row_number = len(readings_data_frame.index) - 1

        # Get the file name to save
        file_name = self.file_location.split('/')[-1]

        # Create a variable for all the register readings that need saving
        register_readings_to_save = []

        for ob in MeterReading.objects.all():
            ob.delete()

        # Start looping over the rows.
        current_reading_entry = None
        for index, row in readings_data_frame.iterrows():
            # Ignore the first and last rows of the file, not so sure what they are at this point.
            if index in [0, final_row_number]:
                continue

            # For values that are required in their row, save directly. If they're not required, check if they're NaN. This would show an error if we're missing a value

            match row[0]:
                case "026":
                    # Reading data starts with a '26' type row. Following rows are related until the next '26' row.
                    # If we come across a 26 now, save the last reading (if there is one) and start a new one.
                    if current_reading_entry:
                        try:
                            current_reading_entry.save()

                        except IntegrityError:  # required fields missing
                            raise CommandError("Missing some required data.")  # TODO: Add more info.

                    # Start making the reading entry
                    current_reading_entry = MeterReading(
                        file_name=file_name,
                        mpan_number=row[1],
                        bsc_validation_status=row[2],
                    )

                case "027" | "029" | "033":
                    # Site visit information
                    current_reading_entry.data_type_code = row[0]
                    current_reading_entry.site_visit_check_code = row[1]
                    current_reading_entry.site_visit_additional_information = row[2] if not math.isnan(row[2]) else None

                case "028":
                    # 028 Meter/reading types
                    current_reading_entry.meter_serial_number = row[1]
                    current_reading_entry.reading_type = row[2]

                case "030":
                    # Register reading
                    # Determine meter reading flag
                    if row[6] == "T":
                        meter_reading_flag = True
                    elif row[6] == "F":
                        meter_reading_flag = False
                    else:
                        meter_reading_flag = None

                    register_readings_to_save.append(RegisterReading(
                        meter_reading=current_reading_entry,
                        meter_register_id=row[1],
                        reading_date_time=datetime.datetime.strptime(row[2], "%Y%m%d%H%M%S"),
                        register_reading=row[3],
                        md_reset_date_time=datetime.datetime.strptime(row[4], "%Y%m%d%H%M%S") if not math.isnan(row[4]) else None,
                        number_of_md_resets=row[5] if not math.isnan(row[5]) else None,
                        meter_reading_flag=meter_reading_flag,
                        reading_method=row[7],
                    ))

                case "32":
                    # Meter Reading Validation Result
                    current_reading_entry.meter_reading_reason_code = row[1]
                    current_reading_entry.meter_reading_status = (True if row[2] == "T" else False)

        # Save the final meter reading
        if current_reading_entry:
            current_reading_entry.save()

        # Create the register readings
        RegisterReading.objects.bulk_create(register_readings_to_save, update_fields=[
            "meter_register_id",
            "reading_date_time",
            "register_reading",
            "md_reset_date_time",
            "number_of_md_resets",
            "meter_reading_flag",
            "reading_method"
        ])
