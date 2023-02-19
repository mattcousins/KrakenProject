from django.db import models


class MeterReading(models.Model):
    BSC_VALIDATION_STATUS_CHOICES = [
        ("F", "Failed"),
        ("U", "Not validated"),
        ("V", "Validated"),
    ]

    READING_TYPE_CHOICES = [
        ("A", "Actual Change of Supplier Read"),
        ("C", "Customer own read"),
        ("D", "Deemed (Settlement Registers) or Estimated (Non-Settlement Registers)"),
        ("F", "Final"),
        ("I", "Initial"),
        ("R", "MAR"),
        ("O", "Old Supplier's Estimated CoS Reading"),
        ("P", "Electronically collected via PPMIP"),
        ("Q", "Meter Reading modified manually by DC"),
        ("R", "Routine"),
        ("S", "Special"),
        ("T", "Proving Test Reading"),
        ("W", "Withdrawn"),
        ("Z", "Actual Change of Tenancy Read"),
    ]

    METER_READING_REASON_CODE_CHOICES = [
        ("01", "MSID Incorrect"),
        ("02", "Reading Dates"),
        ("03", "Negative Consumption"),
        ("04", "Inconsistent with slave register advance"),
        ("05", "Consumption exceeds twice expected advance"),
        ("06", "Meter incorrectly energised"),
        ("07", "Meter incorrectly de-energised"),
        ("08", "Full Scale MD"),
        ("09", "Zero MD"),
        ("10", "Number of MD resets >1"),
        ("11", "Number of register digits incorrect"),
        ("12", "Inconsistent register read date"),
        ("13", "Faulty Meter"),
        ("14", "Hand Held Read Failure"),
        ("15", "Meter Not on Site/Metering protocol not approved"),
        ("16", "Standing Data incorrect"),
        ("17", "No access to meter"),
        ("18", "Meter Time/Date reset"),
        ("19", "Outstation reset"),
        ("20", "Meter Change/Meter Maintenance"),
        ("21", "Phase Failure"),
        ("22", "Meters Recording Zeros"),
        ("23", "Test Data Recorded"),
        ("24", "Data Lapse"),
        ("25", "Actual Data Manually Keyed"),
        ("26", "Invalid Zero Advances"),
        ("27", "Zero Consumption"),
    ]

    DATA_TYPE_CODE_CHOICES = [(1, "027"), (2, "029"), (3, "033")]

    # 026 - MPAN Cores
    mpan_number = models.BigIntegerField()
    # For bsc_validation_status, may be better to use a boolean w/ null=Not validated
    bsc_validation_status = models.CharField(max_length=1, choices=BSC_VALIDATION_STATUS_CHOICES)

    # 027, 029, 033 - Site visit information
    site_visit_information_data_type_code = models.CharField(null=True, max_length=3, choices=DATA_TYPE_CODE_CHOICES)  # Record source's code.
    site_visit_check_code = models.CharField(null=True, max_length=2)
    site_visit_additional_information = models.CharField(null=True, max_length=200)

    # 028 - Meter/reading types
    meter_serial_number = models.CharField(max_length=10)
    reading_type = models.CharField(max_length=1, choices=READING_TYPE_CHOICES)

    # 030 - Register readings. Could be multiple, so make own model

    # 032 - Meter Reading Validation Result
    meter_reading_reason_code = models.CharField(max_length=2, choices=METER_READING_REASON_CODE_CHOICES, null=True)
    meter_reading_status = models.BooleanField(choices=[(True, "Valid"), (False, "Suspect")], null=True)

    # File name
    file_name = models.CharField(max_length=255)

    def __str__(self):
        return f"MPAN: {self.mpan_number} data"


class RegisterReading(models.Model):
    READING_METHOD_CHOICES = [
        ("N", "Not viewed by an Agent or Non Site Visit"),
        ("P", "Viewed by an Agent or Site Visit")
    ]

    meter_reading = models.ForeignKey(MeterReading, on_delete=models.PROTECT)

    # 030 - Register readings
    meter_register_id = models.CharField(max_length=2)
    reading_date_time = models.DateTimeField()
    register_reading = models.DecimalField(max_digits=10, decimal_places=1)
    md_reset_date_time = models.DateTimeField(null=True)
    number_of_md_resets = models.IntegerField(null=True)
    meter_reading_flag = models.BooleanField(choices=[(True, "Valid"), (False, "Suspect")], null=True)
    reading_method = models.CharField(max_length=1, choices=READING_METHOD_CHOICES)
