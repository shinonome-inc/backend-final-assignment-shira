from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def index(request):
    return render(request, "accounts/index.html")


def SignUpView(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("home"))
    else:
        form = SignupForm()
    param = {"form": form}
    return render(request, "accounts/signup.html", param)


@login_required
def HomeView(request):
    return render(request, "accounts/home.html")
