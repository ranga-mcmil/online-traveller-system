from django.db import models

from accommodations.models import AccomodationBooking
from accounts.models import User
from activities.models import ActivityBooking

# Create your models here.
class Payment(models.Model):
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    accommodation_booking = models.ForeignKey(AccomodationBooking, on_delete=models.CASCADE, related_name="booking_payments", null=True, blank=True)
    activity_booking = models.ForeignKey(ActivityBooking, on_delete=models.CASCADE, related_name="booking_payments", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    date_created = models.DateTimeField(auto_now_add=True)