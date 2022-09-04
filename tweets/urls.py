from django.urls import path

from . import views

app_name = "tweets"
urlpatterns = [
    path("create/", views.tweet_create_view, name="tweet_create"),
    path("<int:pk>", views.tweet_detail_view, name="tweet_detail"),
    path("<int:pk>/delete", views.tweet_delete_view, name="tweet_delete"),
]
