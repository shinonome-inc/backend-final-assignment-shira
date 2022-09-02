from django.shortcuts import render
from tweets.models import Tweet


def index_view(request):
    if request.method == "GET":
        tweet_list = Tweet.objects.all()
        context = {"tweet_list": tweet_list}
        return render(request, "welcome/index.html", context)
