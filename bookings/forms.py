# from django import forms
# from .models import Booking


# class BookingForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs.update({'class': 'form-control'})
            
#     class Meta:
#         model = Booking
#         fields = ['start_date', 'end_date']