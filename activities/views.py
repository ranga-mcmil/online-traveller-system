from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic import FormView
from payments.forms import PhoneNumberForm
from payments.models import Payment
from recommendations.forms import SearchForm
# from bookings.forms import BookingForm
from .models import Activity, ActivityBooking
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.utils.timezone import now
from django.forms import DateInput
from django.shortcuts import get_object_or_404
from payments.ecocash import make_payment
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin



class ActivityListView(LoginRequiredMixin, ListView):
  """Renders a list of all activity"""
  model = Activity
  template_name = 'activities/activities_list.html'
  form_class = SearchForm 

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = self.form_class()  # Create a new form instance
    return context
  
  def get_queryset(self):
    queryset = super().get_queryset()  # Get the base queryset

    # Check for search query parameter in URL
    search_query = self.request.GET.get('search')  # Use request.GET for URL parameters

    if search_query:
      # Construct Q objects for case-insensitive search in multiple fields
      queryset = queryset.filter(
         Q(name__icontains=search_query) | Q(destination__name__icontains=search_query)
      )

    return queryset

  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST)

    if form.is_valid():
      search_query = form.get_info()
      url = f"{request.path}?search={search_query}"  # f-string for clean URL construction
      return redirect(url)  # Redirect to the same page with the query parameter

class ActivityDetailView(LoginRequiredMixin, DetailView):
  """Renders details of a specific Activity"""
  model = Activity
  template_name = 'activities/activity_detail.html'


class ActivityBookingCreateView(LoginRequiredMixin, CreateView):
  model = ActivityBooking
  fields = ['date', 'people']  # Fields you want users to edit
  template_name = 'activities/activity_booking.html'  # Adjust as needed

  def get_success_url(self):
    """Dynamically generate success URL with newly created booking ID."""
    booking = self.object  # Access the newly created booking object
    return reverse_lazy('activities:activity_booking_payment', kwargs={'pk': booking.activity.id, 'booking_pk': booking.id})

  def get_form(self, form_class=None):
    form = super(ActivityBookingCreateView, self).get_form(form_class)
    form.fields['date'].widget = DateInput(attrs={'type': 'date', 'min': now().strftime('%Y-%m-%d')})
    for field in form.fields.values():
      field.widget.attrs['class'] = 'form-control' 
    return form

  def form_valid(self, form):
    activity_id = self.kwargs['pk']
    activity = get_object_or_404(Activity, pk=activity_id)
    form.instance.user = self.request.user
    form.instance.activity = activity
    return super().form_valid(form)
  

class ActivityBookingPaymentView(LoginRequiredMixin, FormView):
    template_name = 'accommodations/make_payment.html'
    form_class = PhoneNumberForm
    success_url = reverse_lazy('recommendations:home') 
    
    def get_form_kwargs(self):
        """Inject booking object into the form's initial data."""
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'booking': self.get_booking()}
        return kwargs

    def get_booking(self):
        """Retrieve the booking object based on URL parameter."""
        booking_pk = self.kwargs['booking_pk']
        return get_object_or_404(ActivityBooking, pk=booking_pk)

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
        
