from django import forms
from django.utils.timezone import now


class CheckAvailabilityForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'min': now().strftime('%Y-%m-%d'), 'class': 'form-control', }
    ))
    end_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'min': now().strftime('%Y-%m-%d'), 'class': 'form-control',}
    ))

    def get_info(self):
        # Cleaned data
        cl_data = super().clean()
        start_date = cl_data.get('start_date')
        end_date = cl_data.get('end_date')

        return start_date, end_date
