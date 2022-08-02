from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("", views.index, name="index"),
]
