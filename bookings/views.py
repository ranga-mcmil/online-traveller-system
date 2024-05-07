from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin, View

from accommodations.models import AccomodationBooking
from activities.models import ActivityBooking


# Create your views here.
class BookingsView(TemplateResponseMixin, View):
    template_name = 'bookings/bookings_list.html'

    def get(self, request, *args, **kwargs):
        accommodations_bookings = AccomodationBooking.objects.filter(user=request.user)
        activity_bookings = ActivityBooking.objects.filter(user=request.user)

        context = {
            "accommodations_bookings": accommodations_bookings,
            "activity_bookings": activity_bookings
        }

        return self.render_to_response(context)