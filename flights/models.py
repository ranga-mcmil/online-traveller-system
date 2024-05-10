from django.db import models

from accommodations.models import STATUS
from accounts.models import User
from destinations.models import Destination

# Create your models here.
class Flight(models.Model):
  """Represents a flight to a destination."""
  # origin = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='flights_from')
  # destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='flights_to')
  name = models.CharField(max_length=255, unique=True)
  airline = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def get_flight_origin(self, *args, **kwargs):
    pass

  def get_flight_destination(self, *args, **kwargs):
    pass


class FlightRoute(models.Model):
  """Represents a flight to a destination."""
  flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='flight_routes')
  origin = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='flights_from')
  destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='flights_to')
  price = models.DecimalField(default=0, decimal_places=2, max_digits=20)
  departure = models.DateTimeField()
  arrival = models.DateTimeField()

  def __str__(self):
        return f'{self.origin.name} -> {self.destination.name}'
  

class GeneratedRoute(models.Model):
    """Represents a group of combined flight routes."""
    price = models.DecimalField(default=0, decimal_places=2, max_digits=20)  # New price field
    flight_routes = models.ManyToManyField(FlightRoute)

    def get_name(self, *args, **kwargs):
      if self.flight_routes.count() > 0:
          return self.flight_routes.first().flight.name
      return "untitled"
    
    def get_first_flight_origin(self):
      """Returns the origin name of the first FlightRoute if it exists, otherwise None."""
      if self.flight_routes.count() > 0:
          return self.flight_routes.first().origin.name
      return None

    def get_last_flight_destination(self):
      """Returns the destination name of the last FlightRoute if it exists, otherwise None."""
      if self.flight_routes.count() > 0:
          return self.flight_routes.last().destination.name
      return None
    
    def update_total_price(self):
      self.price = sum(route.price for route in self.flight_routes.all())
      self.save()


class FlightBooking(models.Model):
  """Represents a user's activity booking for a trip."""
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  route = models.ForeignKey(GeneratedRoute, on_delete=models.CASCADE, related_name='bookings')
  people = models.IntegerField(default=1)
  price = models.DecimalField(default=0, decimal_places=2, max_digits=20)
  status = models.CharField(max_length=50, choices=STATUS, default="PENDING")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def save(self, *args, **kwargs):
    # Calculate the price based on your logic (replace with your calculation)
    # This is an example, replace with your actual price calculation logic
    self.price = self.route.price  # Example: Price per person * number of people

    # Call the original save method to persist the data to the database
    super().save(*args, **kwargs)