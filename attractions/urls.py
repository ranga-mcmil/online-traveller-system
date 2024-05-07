from django.urls import path
from . import views

urlpatterns = [
    path('', views.AttractionListView.as_view(), name='attraction_list'),
    path('<int:pk>/', views.AttractionDetailView.as_view(), name='attraction_detail'),
]