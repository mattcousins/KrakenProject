from django.test import TestCase
from django.utils import timezone

from meter_readings.models import MeterReading, RegisterReading


class MeterReadingTestCase(TestCase):
    """
    Test relationship between register readings and meter reading
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meter_reading = None

    def setUp(self):
        # Define a sample to test
        self.meter_reading = MeterReading.objects.create(
            mpan_number=2000055433806,
            bsc_validation_status="V",
            meter_serial_number="D13C01717",
            reading_type="C",
            file_name="test_file.uff",
        )

        RegisterReading.objects.create(
            meter_reading=self.meter_reading,
            meter_register_id="01",
            reading_date_time=timezone.now(),
            register_reading=7242.0,
            reading_method="P",
        )

        RegisterReading.objects.create(
            meter_reading=self.meter_reading,
            meter_register_id="01",
            reading_date_time=timezone.now(),
            register_reading=7500.0,
            reading_method="P",
        )

    def test_meter_reading_relationship(self):
        self.assertEqual(str(self.meter_reading), 'MPAN: 2000055433806 data (2 readings)')
