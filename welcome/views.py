from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.auth import get_user_model

from tweets.models import Tweet
from accounts.models import Connection

User = get_user_model()


@require_GET
def index_view(request):
    tweet_list = Tweet.objects.all().order_by("created_at")
    connection = Connection.objects.get(user=request.user)
    following_list = connection.following.all()
    follower_list = Connection.objects.filter(user=request.user)
    context = {
        "tweet_list": tweet_list,
        "following_list": following_list,
        "follower_list": follower_list,
    }
    return render(request, "welcome/index.html", context)
