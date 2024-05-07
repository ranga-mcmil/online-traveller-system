from django.views.generic import ListView, DetailView
from .models import Destination

class DestinationListView(ListView):
  """Renders a list of all destination"""
  model = Destination
  template_name = 'destinations/destinations_list.html'

class DestinationDetailView(DetailView):
  """Renders details of a specific destination"""
  model = Destination
  template_name = 'destinations/destination_detail.html'
