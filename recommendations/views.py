from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin, View

from accommodations.models import Accommodation
from activities.models import Activity

# Create your views here.
class HomeView(TemplateResponseMixin, View):
    template_name = 'recommendations/home.html'

    def get(self, request, *args, **kwargs):
        accommodations = Accommodation.objects.all()
        activities = Activity.objects.all()

        context = {
            "accommodations": accommodations,
            "activities": activities
        }

        return self.render_to_response(context)