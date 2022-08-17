from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseNotAllowed


def index(request):
    return render(request, "accounts/index.html")


def SignUpView(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignupForm()
    param = {"form": form}
    return render(request, "accounts/signup.html", param)


def LoginView(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "account/login.html", {"form": form})
    elif request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect("home")
        return render(request, "account/login.html", {"form": form})
    return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def LogoutView(request):
    return redirect("home")


@login_required
def HomeView(request):
    return render(request, "accounts/home.html")
