from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView, name="login"),
    path("logout/", views.LogoutView, name="logout"),
    path("home/", views.HomeView, name="home"),
    path("signup/", views.SignUpView, name="signup"),
    path("", views.index, name="index"),
]
