from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .forms import TweetForm
from .models import Like, Tweet


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
    liked_list = Like.objects.filter(user=request.user).values_list("tweet", flat=True)
    the_number_of_likes = tweet.like_set.count()
    context = {
        "tweet": tweet,
        "liked_list": liked_list,
        "the_number_of_likes": the_number_of_likes,
    }
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


@login_required
def like_view(request, pk, *args, **kwargs):
    tweet = get_object_or_404(Tweet, pk=pk)
    Like.objects.get_or_create(user=request.user, tweet=tweet)
    context = {
        "the_number_of_likes": tweet.like_set.count(),
        "tweet.pk": tweet.pk,
    }
    return JsonResponse(context)


@login_required
def unlike_view(request, pk, *args, **kwargs):

    tweet = get_object_or_404(Tweet, pk=pk)
    like = Like.objects.filter(user=request.user, tweet=tweet)

    if like.exists():
        like.delete()
        context = {
            "the_number_of_likes": tweet.like_set.count(),
            "tweet.pk": tweet.pk,
        }
        return JsonResponse(context)
    else:
        raise Http404
