from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, GravatarForm, ProfileSection1Form
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from os import getenv
import random
import hashlib


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            hash = hashlib.md5(
                str(random.getrandbits(128)).encode('utf-8')).hexdigest()
            user.gravatar_link = f"https://www.gravatar.com/avatar/{hash}?d=identicon"
            user.save()
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


@login_required
def index(request):

    return render(request, "accounts/index.html")


@login_required
def profile(request):
    return render(request, "accounts/profile.html")


@login_required
def update_profile(request, section_id):
    user = request.user
    if section_id == 1:
        if request.method == "POST":
            form = ProfileSection1Form(request.POST, instance=user)
            if form.is_valid():
                temp_user = form.save(commit=False)
                user.first_name = temp_user.first_name
                user.last_name = temp_user.last_name
                user.username = temp_user.username
                user.email = temp_user.email
                user.save()
                return redirect(reverse("accounts:profile"))
        else:
            form = ProfileSection1Form(instance=user)
        return render(request, "accounts/profile.html", {
            "form": form,
            f"section{section_id}": True,
        })


@login_required
def change_gravatar(request):
    user = request.user
    if request.method == "POST":
        form = GravatarForm(request.POST)
        if form.is_valid():
            temp_user = form.save(commit=False)
            user.gravatar_link = temp_user.gravatar_link
            user.save()
            return redirect(reverse("accounts:profile"))
    else:
        form = GravatarForm(instance=user)
    return render(request, "accounts/grav_form.html", {
        "form": form,
    })
