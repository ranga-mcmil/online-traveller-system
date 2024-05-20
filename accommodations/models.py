from django.db import models

from accounts.models import User
from destinations.models import Destination

STATUS = (
  ("BOOKED", "BOOKED"),
  ("PENDING", "PENDING"),
  ("CANCELLED", "CANCELLED"),
)

# Create your models here.
class Accommodation(models.Model):
  """Represents accommodation options within a destination."""
  name = models.CharField(max_length=255, unique=True)
  destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='accomodations')
  star_rating = models.IntegerField()
  description = models.TextField()
  pic = models.ImageField(upload_to='images/')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Room(models.Model):
  """Represents room options within an accomodation."""
  name = models.CharField(max_length=255, unique=True)
  accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='rooms')
  room_type = models.CharField(max_length=255)
  price = models.DecimalField(default=0, decimal_places=2, max_digits=20)

class AccomodationBooking(models.Model):
  """Represents a user's accomodation booking for a trip."""
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='bookings')
  room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
  start_date = models.DateTimeField(blank=True, null=True)
  end_date = models.DateTimeField(blank=True, null=True)
  adults = models.IntegerField(blank=True, null=True)
  children = models.IntegerField(blank=True, null=True)
  notes = models.CharField(max_length=255, blank=True, null=True)
  price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  status = models.CharField(max_length=50, choices=STATUS, default="PENDING")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def save(self, *args, **kwargs):
    people = self.children + self.adults
    self.price = self.room.price * people
    super().save(*args, **kwargs)



  
