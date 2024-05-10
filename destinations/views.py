from django.views.generic import ListView, DetailView
from .models import Destination
from django.contrib.auth.mixins import LoginRequiredMixin


class DestinationListView(LoginRequiredMixin, ListView):
  """Renders a list of all destination"""
  model = Destination
  template_name = 'destinations/destinations_list.html'

class DestinationDetailView(LoginRequiredMixin, DetailView):
  """Renders details of a specific destination"""
  model = Destination
  template_name = 'destinations/destination_detail.html'
