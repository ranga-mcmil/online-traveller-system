from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.BookingsView.as_view(), name='bookings'),
]