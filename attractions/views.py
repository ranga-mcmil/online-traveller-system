from django.views.generic import ListView, DetailView
from .models import Attraction

class AttractionListView(ListView):
  """Renders a list of all Attractions"""
  model = Attraction
  template_name = 'attractions/attractions_list.html'

class AttractionDetailView(DetailView):
  """Renders details of a specific Attraction"""
  model = Attraction
  template_name = 'attractions/attraction_detail.html'
