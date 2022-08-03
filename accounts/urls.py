from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.HomeView, name="home"),
    path("signup/", views.SignUpView, name="signup"),
    path("", views.index, name="index"),
]
