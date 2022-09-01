from django.urls import path

from . import views

app_name = "tweets"
urlpatterns = [
    path("create/", views.tweet_create_view, name="create"),
    path("tweets/<int:tweet_id>", views.tweet_detail_view, name="detail"),
    path("tweets/<int:tweet_id>/delete", views.delete_tweet_view, name="delete"),
]
