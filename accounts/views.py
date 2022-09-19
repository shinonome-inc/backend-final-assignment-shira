from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model

from .forms import SignupForm, LoginForm
from .models import Connection


User = get_user_model()


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            connection = Connection(user=user)
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
    follow_user = User.objects.get(username=username)
    connection = Connection.objects.get(user=request.user)
    connection.following.add(follow_user)
    return redirect("welcome:index")


def unfollow_view(request, username):
    unfollow_user = User.objects.get(username=username)
    connection = Connection.objects.get(user=request.user)
    connection.following.remove(unfollow_user)
    return redirect("welcome:index")


def following_list_view(request, username):
    connection = Connection.objects.get(user=request.user)
    following_list = connection.following.all()
    follower_list = User.objects.filter(connection__following=request.user)
    context = {
        "following_list": following_list,
        "follower_list": follower_list,
    }
    return render(request, "accounts/following_list.html", context)


def follower_list_view(request, username):
    connection = Connection.objects.get(user=request.user)
    following_list = connection.following.all()
    follower_list = User.objects.filter(connection__following=request.user)
    context = {
        "following_list": following_list,
        "follower_list": follower_list,
    }
    return render(request, "accounts/follower_list.html", context)
