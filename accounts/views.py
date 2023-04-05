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
            user = form.save()
            send_mail(
                subject="Register in My App",
                message=f"Thanks for registering {user.username.title()}. Hope you'll have fun.",
                from_email=getenv("EMAIL"),
                recipient_list=[user.email],
            )
            return redirect("/accounts/login")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("/")
