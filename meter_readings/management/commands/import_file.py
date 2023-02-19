from abc import ABC

from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Imports a J0010 DTC file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('file_location', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write('Starting to uploaded file.')

        return
