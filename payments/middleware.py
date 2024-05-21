from django.utils.deprecation import MiddlewareMixin
from accommodations.models import AccomodationBooking
from activities.models import ActivityBooking
from flights.models import FlightBooking
from payments.models import Payment
from django.contrib import messages
from django.shortcuts import get_object_or_404
from paynow import Paynow
import time


paynow = Paynow(
    '18546', 
    'dfb5b164-0f03-4b43-b553-0ddc9803da2a',
    'http://example.com/gateways/paynow/update', 
    'http://example.com/return?gateway=paynow'
)

class MyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # This method runs before the view is called for each request
        data_key = request.session.get('data_key', None)

        if data_key:
            poll_url = data_key['poll_url']
            booking_id = data_key['booking_id']
            booking_type = data_key['booking_type']

            request.session.pop('data_key', None)

            i = 0
            while i < 5:
                status = paynow.check_transaction_status(poll_url)

                if status.status == 'paid':
                    self.complete_payment(request, booking_id, booking_type)
                    messages.success(request, "Booked successfully")
                    break

                if status.status == 'cancelled':
                    messages.warning(request, "Payment Transaction Cancelled")
                    break                
                time.sleep(1)
                i += 1      

    def complete_payment(self, request, booking_id, booking_type):
        if booking_type == 'Activity':
            booking = get_object_or_404(ActivityBooking, pk=booking_id)
            booking.status = "BOOKED"
            booking.save()
            Payment.objects.create(amount = 0, activity_booking=booking, user=request.user)
        elif booking_type == 'Accommodation':
            booking = get_object_or_404(AccomodationBooking, pk=booking_id)
            booking.status = "BOOKED"
            booking.save()
            Payment.objects.create(amount = 0,accommodation_booking=booking,user=request.user)
        elif booking_type == 'Flight':
            booking = get_object_or_404(FlightBooking, pk=booking_id)
            booking.status = "BOOKED"
            booking.save()
            Payment.objects.create(amount = 0,flight_booking=booking,user=request.user)
