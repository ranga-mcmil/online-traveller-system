from django.db import models

from destinations.models import Destination

# Create your models here.

class Attraction(models.Model):
  """Represents a point of interest within a destination."""
  name = models.CharField(max_length=255, unique=True)
  image = models.ImageField(models.ImageField(upload_to='images/'))
  destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)