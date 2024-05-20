from django.db import models

from accommodations.models import STATUS
from accounts.models import User
from destinations.models import Destination

# Create your models here.
class Activity(models.Model):
  """Represents activities offered within a destination."""
  name = models.CharField(max_length=255, unique=True)
  destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
  category = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  image = models.ImageField(models.ImageField(upload_to='images/'))
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class ActivityBooking(models.Model):
  """Represents a user's activity booking for a trip."""
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='bookings')
  date = models.DateTimeField(blank=True, null=True)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  people = models.IntegerField()
  status = models.CharField(max_length=50, choices=STATUS, default="PENDING")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def save(self, *args, **kwargs):
    self.price = self.activity.price * self.people
    super().save(*args, **kwargs)
