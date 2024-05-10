from django.urls import path
from . import views


app_name = 'flights'
urlpatterns = [
    path('', views.FlightSearchView.as_view(), name='flight_search'),
    path('<int:pk>/', views.FlightDetailView.as_view(), name='flight_detail'),
    path('<int:pk>/generated-route/', views.GeneratedRouteView.as_view(), name='generated_route'),

    path('<int:pk>/booking/create', views.FlightBookingCreateView.as_view(), name='flight_booking'),
    path('<int:booking_pk>/make-payment/', views.FlightBookingPaymentView.as_view(), name='flight_booking_payment'),

]