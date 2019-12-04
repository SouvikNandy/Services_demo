from django.urls import path
from Services import views

urlpatterns = [
    path('services/', views.ServicesAPIView.as_view()),
    path('available-features/', views.FeaturesAPIView.as_view()),
]
