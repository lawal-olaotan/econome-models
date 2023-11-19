from django.urls import path
from .views import ChatAppView
from django.conf import settings

urlpatterns = [
    path('api', ChatAppView.as_view()),
]