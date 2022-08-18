from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home_view, name="home"),
    path("signup/", views.signup_view, name="signup"),
    path("", views.index_view, name="index"),
]
