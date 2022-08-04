from django.urls import include, path
from . import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("home/", views.HomeView, name="home"),
    path("signup/", views.SignUpView, name="signup"),
    path("welcome", views.index, name="index"),
]
