from django.urls import path
from . import views

app_name = "activities"

urlpatterns = [
    path('', views.ActivityListView.as_view(), name='activity_list'),
    path('<int:pk>/', views.ActivityDetailView.as_view(), name='activity_detail'),
    path('<int:pk>/reviews/', views.ActivityReviewListView.as_view(), name='activity_reviews'),
    path('<int:pk>/booking/create', views.ActivityBookingCreateView.as_view(), name='book'),
    path('<int:pk>/make-payment/<int:booking_pk>/', views.ActivityBookingPaymentView.as_view(), name='activity_booking_payment'),

]