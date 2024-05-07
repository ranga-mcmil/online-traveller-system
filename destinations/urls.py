from django.urls import path
from . import views

urlpatterns = [
    path('', views.DestinationListView.as_view(), name='destination_list'),
    path('<int:pk>/', views.DestinationDetailView.as_view(), name='destination_detail'),
]