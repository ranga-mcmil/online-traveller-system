from django.db import models

# Create your models here.

class Destination(models.Model):
  """Represents a travel destination."""
  name = models.CharField(max_length=255, unique=True)
  country = models.CharField(max_length=255)
  description = models.TextField()
  image = models.ImageField(models.ImageField(upload_to='images/'))
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)