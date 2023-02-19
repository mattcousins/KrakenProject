from django.contrib import admin

from meter_readings.models import MeterReading, RegisterReading


@admin.register(MeterReading)
class MeterReadingAdmin(admin.ModelAdmin):
    pass


@admin.register(RegisterReading)
class RegisterReadingAdmin(admin.ModelAdmin):

    search_fields = ["meter_reading__mpan_number", "meter_reading__meter_serial_number"]
    list_display = [
            "get_mpan_number",
            "get_serial_number",
            "reading_date_time",
            "register_reading",
            "get_file_name"
        ]

    @admin.display(ordering='meter_reading__mpan_number', description='MPAN number')
    def get_mpan_number(self, obj):
        return obj.meter_reading.mpan_number

    @admin.display(ordering='meter_reading__meter_serial_number', description='Serial number')
    def get_serial_number(self, obj):
        return obj.meter_reading.meter_serial_number

    @admin.display(ordering='meter_reading__file_name', description='Import file name')
    def get_file_name(self, obj):
        return obj.meter_reading.file_name
