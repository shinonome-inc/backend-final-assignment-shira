from django.urls import path, include

from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("", include("welcome.urls")),
]
