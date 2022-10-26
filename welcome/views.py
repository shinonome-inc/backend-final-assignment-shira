from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.auth import get_user_model

from tweets.models import Tweet, Like

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
        liked_list = Like.objects.filter(user=request.user).values_list(
            "tweet", flat=True
        )
        context = {
            **context,
            "follower_list": follower_list,
            "followee_list": followee_list,
            "liked_list": liked_list,
        }
    return render(request, "welcome/index.html", context)
