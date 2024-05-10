from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateResponseMixin, View
from django.shortcuts import get_object_or_404
from destinations.models import Destination
from flights.forms import FlightForm
from payments.ecocash import make_payment
from payments.forms import PhoneNumberForm
from payments.models import Payment
# from bookings.forms import BookingForm
from .models import Flight, FlightBooking, FlightRoute, GeneratedRoute
from django.shortcuts import redirect
from django.views.generic import FormView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages



class FlightDetailView(DetailView):
  """Renders details of a specific destination"""
  model = Flight
  template_name = 'flights/flight_detail.html'

class FlightSearchView(FormView):
  template_name = 'flights/flights_search.html'
  form_class = FlightForm

  def get(self, request, *args, **kwargs):
    form = self.get_form()

    origin = self.request.GET.get('origin') 
    destination = self.request.GET.get('destination') 
    generated_route = None

    if origin and destination:
      flight_routes_ = FlightRoute.objects.filter(origin__name__iexact=origin)

      new_paths = self.search_flights(destination, flight_routes_)

      if len(new_paths):
        generated_route = GeneratedRoute.objects.create()

        for flight_route in new_paths:
            generated_route.flight_routes.add(flight_route)

        generated_route.save()
        generated_route.update_total_price()
        generated_route.save()
      
    context = self.get_context_data(form=form, generated_route=generated_route)
    return self.render_to_response(context)

  def form_valid(self, form):    
    origin, destination = form.get_info()
    url = f"{self.request.path}?origin={origin}&destination={destination}"  # f-string for clean URL construction
    return redirect(url)  # Redirect to the same page with the query parameter
    

  def search_flights(self, destination, flight_routes_):
      new_paths = []

      for flight_route in flight_routes_:
        flight = flight_route.flight
        paths = list(flight.flight_routes.all())
        routes_of_flight = list(flight.flight_routes.filter(destination__name__iexact=destination))

        origin_index = paths.index(flight_route)

        try: 
          destination_index = paths.index(routes_of_flight[0])
        except: 
          destination_index = -1

        if origin_index < destination_index:
          for i in range(origin_index, destination_index + 1):
            new_paths.append(paths[i])
        elif origin_index == destination_index:
          new_paths.append(paths[origin_index])

        if len(new_paths) != 0:
          break
      return new_paths


class GeneratedRouteView(DetailView):
  """Renders details of a specific destination"""
  model = GeneratedRoute
  template_name = 'flights/generated_route.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    generated_route = self.object  # Access the GeneratedRoute object
    context['generated_route'] = generated_route
    return context
  
class FlightBookingCreateView(CreateView):
  model = FlightBooking
  fields = ['people']  # Fields you want users to edit
  template_name = 'flights/flight_booking.html'  # Adjust as needed

  def get_success_url(self):
    """Dynamically generate success URL with newly created booking ID."""
    booking = self.object  # Access the newly created booking object
    return reverse_lazy('flights:flight_booking_payment', kwargs={'booking_pk': booking.id})

  def get_form(self, form_class=None):
    form = super(FlightBookingCreateView, self).get_form(form_class)
    for field in form.fields.values():
      field.widget.attrs['class'] = 'form-control' 
    return form

  def form_valid(self, form):
    route_pk = self.kwargs['pk']
    route = get_object_or_404(GeneratedRoute, pk=route_pk)
    form.instance.user = self.request.user
    form.instance.route = route
    return super().form_valid(form)


class FlightBookingPaymentView(FormView):
    template_name = 'accommodations/make_payment.html'
    form_class = PhoneNumberForm
    # success_url = reverse_lazy('activity_booking_payment_success', kwargs={'activity_id': '<activity_id>', 'booking_id': '<booking_id>'})  # Placeholder for actual URL pattern

    def get_form_kwargs(self):
        """Inject booking object into the form's initial data."""
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'booking': self.get_booking()}
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking = self.get_booking()
        print('')
        print('')
        print('')
        print('')
        print('')
        print('')
        print('')
        print(booking.price)
        print('')
        print('')
        print('')
        print('')
        print('')
        print('')
        print('')
        print('')

        context['booking'] = self.get_booking()  # Access the booking object
        # Add other context data as needed (e.g., additional information)
        return context

    def get_booking(self):
        """Retrieve the booking object based on URL parameter."""
        booking_pk = self.kwargs['booking_pk']
        return get_object_or_404(FlightBooking, pk=booking_pk)

    def form_valid(self, form):
        
        # ... (payment processing logic as before)
        phone_number = form.cleaned_data['phone_number']
        # activity_id = self.kwargs['pk']
        booking = self.get_booking()

        try:
            payment_status = make_payment(f'Booking ', phone_number, self.request.user.email, 1)['status']
        except:
            messages.error(self.request, 'Something happened, make sure you are connected to the internet to complete Ecocash payment')
            return redirect(self.request.META['HTTP_REFERER'])
        
        if payment_status == 'paid':
            booking.status = "BOOKED"
            booking.save()

            Payment.objects.create(
              amount = 0,
              activity_booking=booking,
              user=self.request.user
            )
            messages.success(self.request, "Booked successfully")
            return redirect('activities:activity_list')
        elif payment_status == 'sent':
            messages.error(self.request, 'Ecocash prompt sent, could not get confirmation from user. Please try again')
            return redirect(self.request.META['HTTP_REFERER'])
        else:
            messages.error(self.request, 'Error happened, please try again')
            return redirect(self.request.META['HTTP_REFERER'])
        




        