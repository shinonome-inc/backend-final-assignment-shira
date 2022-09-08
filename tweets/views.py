from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import PermissionDenied

from .forms import TweetForm
from .models import Tweet


def tweet_create_view(request):
    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect("welcome:index")
    else:
        form = TweetForm()
    context = {"form": form}
    return render(request, "tweets/create.html", context)


def tweet_detail_view(request, pk):
    tweet = Tweet.objects.get(pk=pk)
    context = {"tweet": tweet}
    return render(request, "tweets/detail.html", context)


def tweet_delete_view(request, pk):
    template_name = "tweets/delete.html"
    tweet = get_object_or_404(Tweet, pk=pk)
    context = {"tweet": tweet}
    if tweet.user == request.user:
        if request.method == "POST":
            tweet.delete()
            return redirect("welcome:index")
        return render(request, template_name, context)
    else:
        raise PermissionDenied
