from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.mixins import LoginRequiredMixin
from accommodations.models import AccomodationBooking
from activities.models import ActivityBooking
from flights.models import FlightBooking


# Create your views here.
class BookingsView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'bookings/bookings_list.html'

    def get(self, request, *args, **kwargs):
        accommodations_bookings = AccomodationBooking.objects.filter(user=request.user).order_by('-id')
        activity_bookings = ActivityBooking.objects.filter(user=request.user).order_by('-id')
        flight_bookings = FlightBooking.objects.filter(user=request.user).order_by('-id')

        print("FLIGHT BOOKINGS", flight_bookings)

        context = {
            "accommodations_bookings": accommodations_bookings,
            "activity_bookings": activity_bookings,
            "flight_bookings": flight_bookings
        }

        return self.render_to_response(context)