from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import TemplateResponseMixin, View
from django.db.models import Q
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.urls import reverse_lazy
from django.forms import ChoiceField, DateInput
from django.urls import reverse
from accommodations.forms import CheckAvailabilityForm
from payments.forms import PhoneNumberForm
from payments.models import Payment
from django.views.generic import FormView

from recommendations.forms import SearchForm
from .models import Accommodation, AccomodationBooking, Room
from django import forms
from payments.ecocash import make_payment
from django.contrib import messages

class AccommodationListView(ListView):
  """Renders a list of all accommodations"""
  model = Accommodation
  template_name = 'accommodations/accommodation_list.html'
  form_class = SearchForm 

  def get_queryset(self):
    queryset = super().get_queryset()  # Get the base queryset

    # Check for search query parameter in URL
    search_query = self.request.GET.get('search')  # Use request.GET for URL parameters

    if search_query:
      # Construct Q objects for case-insensitive search in multiple fields
      queryset = queryset.filter(
         Q(name__icontains=search_query) | Q(description__icontains=search_query) | Q(destination__name__icontains=search_query)
      )

    return queryset
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = self.form_class()  # Create a new form instance
    return context
  
  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST)

    if form.is_valid():
      search_query = form.get_info()
      url = f"{request.path}?search={search_query}"  # f-string for clean URL construction
      return redirect(url)  # Redirect to the same page with the query parameter
      


# class AccommodationDetailView(DetailView):
#   """Renders details of a specific accommodation"""
#   model = Accommodation
#   template_name = 'accommodations/accommodation_detail.html'


class AccommodationDetailView(DetailView):
  """Renders details of a specific accommodation with availability check"""
  model = Accommodation
  template_name = 'accommodations/accommodation_detail.html'
  form_class = CheckAvailabilityForm  # Define the form class

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = self.form_class()  # Create a new form instance
    return context

  def post(self, request, pk, *args, **kwargs):
    form = self.form_class(request.POST)
    accommodation = self.get_object()  # Retrieve the accommodation object

    if form.is_valid():
      start_date, end_date = form.get_info()

      # Find conflicting bookings
      conflicting_bookings = AccomodationBooking.objects.filter(
          Q(accommodation=accommodation),
          Q(
              Q(start_date__lte=end_date) & Q(end_date__gte=start_date) |  # Overlapping booking
              Q(start_date__gte=start_date) & Q(end_date__lte=end_date) |  # Booking entirely within selected dates
              Q(start_date__lt=start_date) & Q(end_date__gt=end_date)   # Booking surrounds selected dates
          )
      )

      # Get all rooms and exclude those with conflicting bookings
      all_rooms = accommodation.rooms.all()
      available_rooms = all_rooms.exclude(bookings__in=conflicting_bookings)

      context = {
          "accommodation": accommodation,
          "form": form,
          "start_date": str(start_date),
          "end_date": str(end_date),
          "available_rooms": available_rooms,
      }

      return render(request, self.template_name, context)

    # Display the form with any errors
    context = {
        "accommodation": accommodation,
        "form": form,
    }
    return render(request, self.template_name, context)


class CheckAvailabilityView(TemplateResponseMixin, View):
    template_name = 'accommodations/check_availability.html'
    accommodation = None
    request = None

    def dispatch(self, request, pk, *args, **kwargs):
      self.accommodation = get_object_or_404(Accommodation, pk=pk)
      self.request = request
      return super().dispatch(request)
    
    def get(self, pk):
      form = CheckAvailabilityForm()
      context = {
        "accommodation": self.accommodation,
        "form": form
      }
      return self.render_to_response(context)

    def post(self, pk):
      form = CheckAvailabilityForm(data=self.request.POST)

      if form.is_valid():
        start_date, end_date = form.get_info()

        # Find all bookings that conflict with the selected dates
        conflicting_bookings = AccomodationBooking.objects.filter(
          Q(accommodation=self.accommodation),
          Q(
            Q(start_date__lte=end_date) & Q(end_date__gte=start_date) |  # Overlapping booking
            Q(start_date__gte=start_date) & Q(end_date__lte=end_date) |  # Booking entirely within selected dates
            Q(start_date__lt=start_date) & Q(end_date__gt=end_date)      # Booking surrounds selected dates
          )
        )

        # Get all rooms for this accommodation
        all_rooms = self.accommodation.rooms.all()

        # Exclude rooms with conflicting bookings
        available_rooms = all_rooms.exclude(bookings__in=conflicting_bookings)

        # Add available rooms to context and render the template
        context = {
          "accommodation": self.accommodation,
          "form": form,
          "start_date": str(start_date),
          "end_date": str(end_date),
          "available_rooms": available_rooms,
        }
        return self.render_to_response(context)
    
class AccommodationBookingView(CreateView):
    model = AccomodationBooking
    fields = ["start_date", "end_date", "adults", "children", "notes"]
    success_message = f"The booking saved ."
    template_name = 'accommodations/accommodation_booking.html'
    accommodation = None
    room = None
    start_date = None
    end_date = None
    request = None

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['accommodation'] = self.accommodation
      return context
    
    def get_success_url(self):
      """Dynamically generate success URL with newly created booking ID."""
      booking = self.object  # Access the newly created booking object
      return reverse_lazy('accommodations:accommodation_booking_payment', kwargs={'pk': booking.accommodation.id, 'booking_pk': booking.pk})

    def dispatch(self, request, pk, room_pk, start_date, end_date, *args, **kwargs):
      self.accommodation = get_object_or_404(Accommodation, pk=pk)
      self.room = get_object_or_404(Room, pk=room_pk)
      self.start_date = start_date
      self.end_date = end_date
      self.request = request
      return super().dispatch(request)

    def get_form(self, form_class=None):
      form = super(AccommodationBookingView, self).get_form(form_class)
      
      # Define choices for adults and children fields
      adults_choices = [(str(i), str(i)) for i in range(1, 6)]  # Adjust MAX_ADULTS as needed
      children_choices = [(str(i), str(i)) for i in range(6)]  # Adjust MAX_CHILDREN as needed

      # Update fields with ChoiceFields
      form.fields['adults'] = ChoiceField(label='Adults', choices=adults_choices)
      form.fields['children'] = ChoiceField(label='Children', choices=children_choices)
      form.fields['notes'] = forms.CharField(widget=forms.Textarea)
      form.fields['start_date'].widget = DateInput(attrs={'type': 'date', 'disabled': True, 'required': False, 'value': self.start_date})
      form.fields['end_date'].widget = DateInput(attrs={'type': 'date', 'disabled': True, 'required': False, 'value': self.end_date})

      for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control' 
      return form
    
    def form_valid(self, form):
      form.instance.accommodation = self.accommodation
      form.instance.room = self.room
      form.instance.start_date = self.start_date
      form.instance.end_date = self.end_date
      form.instance.user = self.request.user
      return super().form_valid(form)

# class AccommodationBookingPaymentView(TemplateResponseMixin, View):
#     template_name = 'accommodations/make_payment.html'
#     booking = None
#     request = None

#     def dispatch(self, request, booking_pk, *args, **kwargs):
#       self.booking = get_object_or_404(AccomodationBooking, pk=booking_pk)
#       self.request = request
#       return super().dispatch(request)
    
#     def get(self, pk):
#       form = PhoneNumberForm()
#       context = {
#         "booking": self.booking,
#         "form": form
#       }
#       return self.render_to_response(context)
    
#     def post(self, pk):
#       form = PhoneNumberForm(data=self.request.POST)

#       if form.is_valid():
#         phone_number = form.get_info()

#         # Set booking status to booked from pending
#         self.booking.status = "BOOKED"
#         self.booking.save()

#         Payment.objects.create(
#           amount = self.booking.room.price,
#           accommodation_booking=self.booking,
#           user=self.request.user
#         )
    

class AccommodationBookingPaymentView(FormView):
    template_name = 'accommodations/make_payment.html'
    form_class = PhoneNumberForm
    request = None
    # success_url = reverse_lazy('activity_booking_payment_success', kwargs={'activity_id': '<activity_id>', 'booking_id': '<booking_id>'})  # Placeholder for actual URL pattern

    def dispatch(self, request, booking_pk, *args, **kwargs):
      self.request = request
      return super().dispatch(request)

    def get_form_kwargs(self):
        """Inject booking object into the form's initial data."""
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'booking': self.get_booking()}
        return kwargs

    def get_booking(self):
        """Retrieve the booking object based on URL parameter."""
        booking_pk = self.kwargs['booking_pk']
        return get_object_or_404(AccomodationBooking, pk=booking_pk)
    
    def get_accommodation(self):
        """Retrieve the booking object based on URL parameter."""
        booking_pk = self.kwargs['booking_pk']
        return get_object_or_404(AccomodationBooking, pk=booking_pk)

    def form_valid(self, form):
        # ... (payment processing logic as before)
        phone_number = form.cleaned_data['phone_number']
        
        activity_id = self.kwargs['pk']
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
              accommodation_booking=booking,
              user=self.request.user
            )
            messages.success(self.request, "Booked successfully")
            return redirect('accommodations:accommodation_list')
        elif payment_status == 'sent':
            messages.error(self.request, 'Ecocash prompt sent, could not get confirmation from user. Please try again')
            return redirect(self.request.META['HTTP_REFERER'])
        else:
            messages.error(self.request, 'Error happened, please try again')
            return redirect(self.request.META['HTTP_REFERER'])

class SearchResultsView(ListView):
    model = Accommodation
    template_name = 'search_results.html'
    paginate_by = 10  # Optional: Paginate results (10 per page)

    def get_queryset(self):
        """
        Filters accommodations using Q objects for flexible search criteria.
        """
        search_query = self.request.GET.get('q', '')

        if search_query:
            # Construct Q object for case-insensitive search in multiple fields
            q_object = Q(name__icontains=search_query) | Q(description__icontains=search_query)
            queryset = Accommodation.objects.filter(q_object)
        else:
            queryset = Accommodation.objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context