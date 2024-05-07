from django.urls import path
from . import views


app_name = 'flights'
urlpatterns = [
    path('', views.FlightListView.as_view(), name='flight_list'),
    path('<int:pk>/', views.FlightDetailView.as_view(), name='flight_detail'),
    # path('<int:pk>/booking/', views.FlightBookingView.as_view(), name='accommodation_booking'),

]