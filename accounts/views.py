from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, GravatarForm, ProfileSection1Form, ProfileSection2Form
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from os import getenv
import random
from django.contrib.auth.models import Group
import hashlib
from django.contrib.auth import get_user_model


USER = get_user_model()


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

                public = form.cleaned_data.get("public")
                group = Group.objects.filter(name="public account").first()
                if group:
                    if public == "True" and not user.groups.filter(name=group.name).exists():
                        print("add")
                        group.user_set.add(user)
                    elif public == "False" and user.groups.filter(name=group.name).exists():
                        print("del")
                        group.user_set.remove(user)
                else:
                    return HttpResponse("Error: Group not found")
                return redirect(reverse("accounts:profile"))

        else:
            form = ProfileSection1Form(instance=user)

    if section_id == 2:
        if request.method == "POST":
            form = ProfileSection2Form(request.POST)
            if form.is_valid():
                quote_newsletter = form.cleaned_data.get("quote_newsletter")
                group = Group.objects.filter(name="quote newsletter").first()
                if group:
                    if quote_newsletter == "True" and not request.user.groups.filter(name=group.name).exists():
                        group.user_set.add(request.user)
                    elif quote_newsletter == "False" and request.user.groups.filter(name=group.name).exists():
                        group.user_set.remove(request.user)
                    return redirect(reverse("accounts:profile"))
                else:
                    return HttpResponse("Error: Group not found")
        else:
            form = ProfileSection2Form()
        return render(request, "accounts/profile.html", {
            "form": form,
            f"section{section_id}": True,
        })
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


@login_required
def public_users(request):

    public_users = USER.objects.filter(
        groups__name="public account").exclude(id=request.user.id)

    return render(request, "accounts/public_users.html", {
        "public_users": public_users,
    })


@login_required
def send_friend_request(request, friend_id):

    def check(u1, u2):
        if u1.requested_friends.filter(id=u2.id).exists() and u2.requested_friends.filter(id=u1.id).exists():
            u1.requested_friends.remove(u2)
            u2.requested_friends.remove(u1)
            u1.friends.add(u2)
            #TODO Wow, You are now friends. Send some message or sth.
        else:
            #TODO Send Notification to second user
            pass


    user = request.user
    new_friend = USER.objects.filter(id=friend_id).first()
    if not user.friends.filter(id=new_friend.id).exists() and not user.requested_friends.filter(id=new_friend.id).exists():
        user.requested_friends.add(new_friend)
        check(user, new_friend)
    return redirect(reverse("accounts:public_users"))

