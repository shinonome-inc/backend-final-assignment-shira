from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(to="/accounts/home/")
    else:
        form = SignupForm()
    param = {"form": form}
    return render(request, "accounts/signup.html", param)


def index(request):
    return render(request, "accounts/index.html")


@login_required
def home(request):
    return render(request, "accounts/home.html")
