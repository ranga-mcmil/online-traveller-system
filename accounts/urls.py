from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.forms import CustomAuthenticationForm
from . import views
from django.urls import reverse_lazy


app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('password-change/', views.PasswordChangeView.as_view(success_url = '/'), name='password_change'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
]