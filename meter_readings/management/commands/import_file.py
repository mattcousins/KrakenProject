from django.core.management import BaseCommand, CommandError

from meter_readings.MeterReadingFileImport import MeterReadingFileImport


class Command(BaseCommand):
    help = 'Imports a J0010 DTC file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('file_location', type=str)

    def handle(self, *args, **options):
        self.stdout.write("Starting to upload file.")

        MeterReadingFileImport(options["file_location"]).import_data_to_database()

        self.stdout.write(self.style.SUCCESS("File successfully uploaded."))

        return
