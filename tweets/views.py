from django.shortcuts import get_object_or_404, redirect, render
from .forms import TweetForm

from .models import Tweet


def tweet_create_view(request):
    if request.method == "POST":
        tweet = TweetForm(request.POST or None)
        if tweet.is_valid():
            form = tweet.save(commit=False)
            form.user = request.user
            form.save()
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
    template_name = "tweets/tweet_delete.html"
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    context = {"tweet": tweet}
    if request.POST:
        tweet.delete()
        return redirect("welcome:index")
    return render(request, template_name, context)
