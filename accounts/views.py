from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model

from .forms import SignupForm, LoginForm
from .models import FollowConnection
from tweets.models import Tweet


User = get_user_model()


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("welcome:index")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                return redirect("welcome:index")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("welcome:index")


def follow_view(request, username):
    follow_user = get_object_or_404(User, username=username)
    if follow_user == request.user:
        return render(request, "welcome/index.html", status=404)
    else:
        FollowConnection.objects.create(follower=request.user, followee=follow_user)
        return redirect("welcome:index")


def unfollow_view(request, username):
    unfollow_user = get_object_or_404(User, username=username)
    if unfollow_user == request.user:
        return render(request, "welcome/index.html", status=404)
    delete_user = get_object_or_404(
        FollowConnection, follower=request.user, followee=unfollow_user
    )
    delete_user.delete()
    return redirect("welcome:index")


def followee_list_view(request, username):
    user = User.objects.prefetch_related("followers", "followees").get(
        username=username
    )
    followee_list = user.followees.all()
    follower_list = user.followers.all()
    context = {
        "username": username,
        "followee_list": followee_list,
        "follower_list": follower_list,
    }
    return render(request, "accounts/followee_list.html", context)


def follower_list_view(request, username):
    user = User.objects.prefetch_related("followers", "followees").get(
        username=username
    )
    followee_list = user.followees.all()
    follower_list = user.followers.all()
    context = {
        "username": username,
        "followee_list": followee_list,
        "follower_list": follower_list,
    }
    return render(request, "accounts/follower_list.html", context)


def user_profile_view(request, username):
    user = User.objects.prefetch_related("followers", "followees").get(
        username=username
    )
    tweet_list = Tweet.objects.filter(user=user).order_by("created_at")
    followee_list = user.followees.all()
    follower_list = user.followers.all()
    context = {
        "username": username,
        "tweet_list": tweet_list,
        "followee_list": followee_list,
        "follower_list": follower_list,
    }
    return render(request, "accounts/profile.html", context)
