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
            followconnection = FollowConnection(follower=user)
            followconnection.save()
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
        return render(request, "welcome/index.html", status=200)
    else:
        followconnection = FollowConnection.objects.get(follower=request.user)
        followee_list = followconnection.followee_list.all()
        if follow_user not in followee_list:
            followconnection.followee_list.add(follow_user)
        return redirect("welcome:index")


def unfollow_view(request, username):
    unfollow_user = get_object_or_404(User, username=username)
    if unfollow_user == request.user:
        return render(request, "welcome/index.html", status=200)
    followconnection = FollowConnection.objects.get(follower=request.user)
    followconnection.followee_list.remove(unfollow_user)
    return redirect("welcome:index")


def followee_list_view(request, username):
    user = User.objects.get(username=username)
    followconnection = FollowConnection.objects.get(follower=user)
    followee_list = followconnection.followee_list.all()
    follower_list = User.objects.filter(followconnection__followee_list=user)
    context = {
        "username": username,
        "followee_list": followee_list,
        "follower_list": follower_list,
    }
    return render(request, "accounts/followee_list.html", context)


def follower_list_view(request, username):
    user = User.objects.get(username=username)
    followconnection = FollowConnection.objects.get(follower=user)
    followee_list = followconnection.followee_list.all()
    follower_list = User.objects.filter(followconnection__followee_list=user)
    context = {
        "username": username,
        "followee_list": followee_list,
        "follower_list": follower_list,
    }
    return render(request, "accounts/follower_list.html", context)


def user_profile_view(request, username):
    user = User.objects.get(username=username)
    tweet_list = Tweet.objects.filter(user=user).order_by("created_at")
    followconnection = FollowConnection.objects.get(follower=user)
    followee_list = followconnection.followee_list.all()
    follower_list = User.objects.filter(followconnection__followee_list=user)
    context = {
        "username": username,
        "tweet_list": tweet_list,
        "followee_list": followee_list,
        "follower_list": follower_list,
    }
    return render(request, "accounts/profile.html", context)
