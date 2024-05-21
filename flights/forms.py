from django import forms
from .models import Destination

class FlightForm(forms.Form):
    origin = forms.ModelChoiceField(queryset=Destination.objects.all(), 
                                    empty_label=None, 
                                    widget=forms.Select(attrs={'class': 'form-control'}))

    destination = forms.ModelChoiceField(queryset=Destination.objects.all(), 
                                        empty_label=None, 
                                        widget=forms.Select(attrs={'class': 'form-control'}))

    def get_info(self):
        # Cleaned data
        cl_data = super().clean()
        origin = cl_data.get('origin')
        destination = cl_data.get('destination')
        return origin, destination