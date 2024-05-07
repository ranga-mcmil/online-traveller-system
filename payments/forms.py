from django import forms

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'val',
            'type': 'number'

        }
    ))

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()
        phone_number = cl_data.get('phone_number')
        return phone_number
