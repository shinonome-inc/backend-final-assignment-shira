from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.auth import get_user_model

from tweets.models import Tweet
from accounts.models import Connection

User = get_user_model()


@require_GET
def index_view(request):
    tweet_list = Tweet.objects.all().order_by("created_at")
    context = {
        "tweet_list": tweet_list,
    }
    if request.user.is_authenticated:
        connection = Connection.objects.get(user=request.user)
        following_list = connection.following.all()
        follower_list = User.objects.filter(connection__following=request.user)
        context = {
            **context,
            "following_list": following_list,
            "follower_list": follower_list,
        }
    return render(request, "welcome/index.html", context)
