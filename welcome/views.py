from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.auth import get_user_model

from tweets.models import Tweet

User = get_user_model()


@require_GET
def index_view(request):
    tweet_list = Tweet.objects.all().order_by("created_at")
    context = {
        "tweet_list": tweet_list,
    }
    if request.user.is_authenticated:
        followee_list = request.user.followees.all()
        follower_list = request.user.followers.all()
        context = {
            **context,
            "follower_list": follower_list,
            "followee_list": followee_list,
        }
    return render(request, "welcome/index.html", context)
