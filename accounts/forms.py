from django import forms
from accounts.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class RegistrationForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())
  confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
        field.widget.attrs.update({'class': 'form-control'})

  def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')
    if password and confirm_password and password != confirm_password:
      raise ValidationError('Passwords don\'t match.')
    return cleaned_data

  class Meta:
    model = User
    fields = ['email', 'password', 'confirm_password']

class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password1"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password2"].widget = forms.PasswordInput(attrs={"class": "form-control"})
