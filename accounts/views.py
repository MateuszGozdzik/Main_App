from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from os import getenv


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            send_mail(
                subject="Thanks for registering in my App",
                message="Thanks for registering. Hope you'll have fun.",
                from_email=getenv("EMAIL"),
                recipient_list=[request.POST["email"]],
            )
            return redirect("/accounts/login")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("/")
