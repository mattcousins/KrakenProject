from django.views.generic import DetailView, ListView

from meter_readings.models import MeterReading


class MeterReadingDetailView(DetailView):
    model = MeterReading


class MeterReadingListView(ListView):
    model = MeterReading
    template_name = "meter_readings/meter_reading_list.html.jinja2"
