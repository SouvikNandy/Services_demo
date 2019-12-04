from django.urls import path
from Client import views

urlpatterns = [
    path('subscription/', views.ClientSubscriptionAPIView.as_view()),
]
