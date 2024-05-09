from django import forms

class FlightForm(forms.Form):
    origin = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    destination = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    def get_info(self):
        # Cleaned data
        cl_data = super().clean()
        origin = cl_data.get('origin')
        destination = cl_data.get('destination')
        return origin, destination
