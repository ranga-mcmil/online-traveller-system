from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin, View
from django.db.models import Q
from accommodations.models import Accommodation
from activities.models import Activity
from recommendations.forms import SearchForm
from django.shortcuts import redirect

# Create your views here.
class HomeView(TemplateResponseMixin, View):
    template_name = 'recommendations/home.html'
    form_class = SearchForm 

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            search_query = form.get_info()
            url = f"{request.path}?search={search_query}"  # f-string for clean URL construction
            return redirect(url)  # Redirect to the same page with the query parameter
        
    def get(self, request, *args, **kwargs):
        accommodations = Accommodation.objects.all()
        activities = Activity.objects.all()

        search_query = self.request.GET.get('search')

        if search_query:
            activities = activities.filter(
                Q(name__icontains=search_query) | Q(destination__name__icontains=search_query)
            )

            accommodations = accommodations.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query) | Q(destination__name__icontains=search_query)
            )

        context = {
            "accommodations": accommodations,
            "activities": activities,
            "form": SearchForm()
        }

        return self.render_to_response(context)