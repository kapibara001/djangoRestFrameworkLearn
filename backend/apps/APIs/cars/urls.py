from django.urls import path
from .views import CarListCreateView, CarDetailView

urlpatterns = [
    path('', CarListCreateView.as_view(), name='cars-list-create'),
    path('<int:pk>', CarDetailView.as_view(), name='car-detail'),
]