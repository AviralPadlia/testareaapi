from django.urls import path
from .views import CalculateAreaView

urlpatterns = [
    path('computeArea', CalculateAreaView.as_view(), name='calculate_area'),  # Example URL pattern
    # Add your app's specific URL patterns here
]
