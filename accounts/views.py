from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic import UpdateView
from accounts.models import User
from .forms import RegistrationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin


class RegistrationView(TemplateResponseMixin, View):
    template_name = 'registration/register.html'
    
    def get(self, request):
        form = RegistrationForm()
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save without actually saving yet 
            user.set_password(user.password)  # Hash password before saving
            user.save()  # Now save the user with the hashed password using custom manager
            login(request, user)  # Log in the newly created user
            return redirect('recommendations:home')  # Redirect to your desired URL after successful registration
        context = {'form': form}
        return self.render_to_response(context)
    
class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "registration/password_change_form.html"

    def form_valid(self, form):
        form.save()
        # messages.success(self.request, "Password updated successfully")
        return super(PasswordChangeView, self).form_valid(form)

class ProfileView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'accounts/profile.html'
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name"]

    def get_form(self, form_class=None):
        form = super(ProfileUpdateView, self).get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        return form

    def get_object(self, queryset=None):
        return self.request.user
    
