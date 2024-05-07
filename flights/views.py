from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateResponseMixin, View
# from bookings.forms import BookingForm
from .models import Flight
from django.shortcuts import redirect


class FlightListView(ListView):
  """Renders a list of all destination"""
  model = Flight
  template_name = 'flights/flights_list.html'

class FlightDetailView(DetailView):
  """Renders details of a specific destination"""
  model = Flight
  template_name = 'flights/flight_detail.html'


# class FlightBookingView(TemplateResponseMixin, View):
#     template_name = 'flights/flight_booking.html'

#     def get(self, request):
#       form = BookingForm()
#       return self.render_to_response({'form': form})
 
#     def post(self, request, id):
#       flight = Flight.objects.get(id=id)
#       form = BookingForm(request.POST)
      
#       if form.is_valid():
#           new_booking = form.save(commit=False)
#           new_booking.flight = flight
#           new_booking.save()
#           return redirect('assessments:home')

#       return self.render_to_response({'form': form})