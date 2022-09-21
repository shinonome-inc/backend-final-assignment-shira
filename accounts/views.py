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
            connection = FollowConnection(user=user)
            connection.save()
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
        connection = FollowConnection.objects.get(user=request.user)
        connection.followee.add(follow_user)
        return redirect("welcome:index")


def unfollow_view(request, username):
    unfollow_user = get_object_or_404(User, username=username)
    if unfollow_user == request.user:
        return render(request, "welcome/index.html", status=200)
    connection = FollowConnection.objects.get(user=request.user)
    connection.followee.remove(unfollow_user)
    return redirect("welcome:index")


def followee_list_view(request, username):
    user = User.objects.get(username=username)
    connection = FollowConnection.objects.get(user=user)
    followee_list = connection.followee.all()
    follower_list = User.objects.filter(followconnection__followee=user)
    context = {
        "username": username,
        "followee_list": followee_list,
        "follower_list": follower_list,
    }
    return render(request, "accounts/followee_list.html", context)


def follower_list_view(request, username):
    user = User.objects.get(username=username)
    connection = FollowConnection.objects.get(user=user)
    followee_list = connection.followee.all()
    follower_list = User.objects.filter(followconnection__followee=user)
    context = {
        "username": username,
        "followee_list": followee_list,
        "follower_list": follower_list,
    }
    return render(request, "accounts/follower_list.html", context)


def user_profile__view(request, username):
    user = User.objects.get(username=username)
    tweet_list = Tweet.objects.filter(user=user).order_by("created_at")
    connection = FollowConnection.objects.get(user=user)
    followee_list = connection.followee.all()
    follower_list = User.objects.filter(followconnection__followee=user)
    context = {
        "username": username,
        "tweet_list": tweet_list,
        "followee_list": followee_list,
        "follower_list": follower_list,
    }
    return render(request, "accounts/profile.html", context)
