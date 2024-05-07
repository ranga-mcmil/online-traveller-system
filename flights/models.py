from django.db import models

from destinations.models import Destination

# Create your models here.
class Flight(models.Model):
  """Represents a flight to a destination."""
  # origin = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='flights_from')
  # destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='flights_to')
  airline = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def get_flight_origin(self, *args, **kwargs):
    pass

  def get_flight_destination(self, *args, **kwargs):
    pass


class FlightPath(models.Model):
  """Represents a flight to a destination."""
  flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='paths')
  destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='path_to')
  departure_date = models.DateTimeField()
  arrival_date = models.DateTimeField()