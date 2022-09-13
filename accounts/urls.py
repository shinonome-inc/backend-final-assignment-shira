from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("<str:username>/follow", views.follow_view, name="follow"),
    path("<str:username>/unfollow", views.unfollow_view, name="unfollow"),
    path("<str:username>/following_list", views.following_list_view, name="following_list"),
    path("<str:username>/follower_list", views.follower_list_view, name="follower_list"),
]
