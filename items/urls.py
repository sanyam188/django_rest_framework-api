from rest_framework import routers
from django.urls import path, include
from .views import UserApiView, ItemApiView, RatingApiView



urlpatterns = [
    path('', include('rest_framework.urls')),
    path('', ItemApiView.as_view()),
    path('user/', UserApiView.as_view()),
    path('product/', ItemApiView.as_view()),
    path('product/<int:pk>/', RatingApiView.as_view())
]
