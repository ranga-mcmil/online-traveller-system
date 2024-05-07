from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic import FormView
from payments.forms import PhoneNumberForm
from payments.models import Payment
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


class ActivityListView(ListView):
  """Renders a list of all activity"""
  model = Activity
  template_name = 'activities/activities_list.html'

class ActivityDetailView(DetailView):
  """Renders details of a specific Activity"""
  model = Activity
  template_name = 'activities/activity_detail.html'


class ActivityBookingCreateView(CreateView):
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
  

class ActivityBookingPaymentView(FormView):
    template_name = 'accommodations/make_payment.html'
    form_class = PhoneNumberForm
    # success_url = reverse_lazy('activity_booking_payment_success', kwargs={'activity_id': '<activity_id>', 'booking_id': '<booking_id>'})  # Placeholder for actual URL pattern

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
        
