from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'val',
        }
    ))

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()
        search = cl_data.get('search')
        return search
