from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.auth import get_user_model

from tweets.models import Tweet
from accounts.models import FollowConnection

User = get_user_model()


@require_GET
def index_view(request):
    tweet_list = Tweet.objects.all().order_by("created_at")
    context = {
        "tweet_list": tweet_list,
    }
    if request.user.is_authenticated:
        followconnection = FollowConnection.objects.get(follower=request.user)
        followee_list = followconnection.followee_list.all()
        follower_list = User.objects.filter(
            followconnection__followee_list=request.user
        )
        context = {
            **context,
            "follower_list": follower_list,
            "followee_list": followee_list,
        }
    return render(request, "welcome/index.html", context)
