from django.urls import path
from . import views

app_name = 'accommodations'

urlpatterns = [
    path('', views.AccommodationListView.as_view(), name='accommodation_list'),
    path('<int:pk>/', views.AccommodationDetailView.as_view(), name='accommodation_detail'),
    path('<int:pk>/check-availability/', views.CheckAvailabilityView.as_view(), name='check_availability'),
    path('<int:pk>/reviews/', views.AccommodationReviewListView.as_view(), name='accommodation_reviews'),
    path('<int:pk>/booking/<int:room_pk>/<str:start_date>/<str:end_date>/', views.AccommodationBookingView.as_view(), name='accommodation_booking'),
    path('<int:pk>/make-payment/<int:booking_pk>/', views.AccommodationBookingPaymentView.as_view(), name='accommodation_booking_payment'),
]