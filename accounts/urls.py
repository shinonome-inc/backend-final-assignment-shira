from django.urls import path, include

from . import views

<<<<<<< HEAD
urlpatterns = [
    path("home/", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
]
