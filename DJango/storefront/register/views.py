from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm
from functools import wraps


def register(request):
    if request.user.is_authenticated:
        form = RegisterForm()
        return render(request, "register/register.html", {"form": form})
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/home")
    else:
        form = RegisterForm()
        return render(request, "register/register.html", {"form": form})
    


    