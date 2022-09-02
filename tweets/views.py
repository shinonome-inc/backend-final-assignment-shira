from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from .forms import TweetForm

from .models import Tweet


def tweet_create_view(request):
    if request.method == "POST":
        form = TweetForm(request.POST or None)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect("welcome:index")
    else:
        tweet = TweetForm()
        context = {"tweet": tweet}
    return render(request, "tweets/tweet_create.html", context)


def tweet_detail_view(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    context = {"tweet": tweet}
    return render(request, "tweets/tweet_detail.html", context)


def tweet_delete_view(request, tweet_id):
    tweet = Tweet.objects.get(pk=tweet_id)
    context = {"tweet": tweet}
    if request.method == "POST":
        if "confirm" in request.POST:
            tweet.delete()
            return redirect("welcome:index")
    return render(request, "tweets/tweet_delete.html", context)
