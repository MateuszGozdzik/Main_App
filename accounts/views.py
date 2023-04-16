import hashlib
import random
from os import getenv

from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import (
    CustomUserCreationForm,
    GravatarForm,
    ProfileSection1Form,
    ProfileSection2Form,
)

from notifications.models import Notification
from notifications.views import add_notification

USER = get_user_model()


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            hash = hashlib.md5(str(random.getrandbits(128)).encode("utf-8")).hexdigest()
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
    return redirect(reverse("accounts:login"))


@login_required
def index(request):
    return render(request, "accounts/index.html")


@login_required
def profile(request):
    return render(request, "accounts/profile.html")


@login_required
def update_profile(request, section_id):
    def change_group(user, group, decision):
        if decision == "True" and not user.groups.filter(name=group.name).exists():
            group.user_set.add(user)
        elif decision == "False" and user.groups.filter(name=group.name).exists():
            group.user_set.remove(user)

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
                change_group(user, group, public)

                return redirect(reverse("accounts:profile"))

        else:
            public_bool = request.user.groups.filter(name="public account").exists()
            form = ProfileSection1Form(instance=user, public_bool=public_bool)

    if section_id == 2:
        if request.method == "POST":
            form = ProfileSection2Form(request.POST)
            if form.is_valid():
                quote_newsletter = form.cleaned_data.get("quote_newsletter")
                quote_group = Group.objects.filter(name="quote newsletter").first()
                change_group(user, quote_group, quote_newsletter)

                email_notifications = form.cleaned_data.get("email_notifications")
                email_group = Group.objects.filter(name="email notifications").first()
                change_group(user, email_group, email_notifications)

                return redirect(reverse("accounts:profile"))
        else:
            quote_bool = request.user.groups.filter(name="quote newsletter").exists()
            email_bool = request.user.groups.filter(name="email notifications").exists()
            form = ProfileSection2Form(quote_bool=quote_bool, email_bool=email_bool)
        return render(
            request,
            "accounts/profile.html",
            {
                "form": form,
                f"section{section_id}": True,
            },
        )
    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            f"section{section_id}": True,
        },
    )


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
    return render(
        request,
        "accounts/grav_form.html",
        {
            "form": form,
        },
    )


@login_required
def public_users(request):
    public_users = USER.objects.filter(groups__name="public account").exclude(
        id=request.user.id
    )

    return render(
        request,
        "accounts/public_users.html",
        {
            "public_users": public_users,
        },
    )


@login_required
def send_friend_request(request, friend_id):
    def check(u1, u2):
        if (
            u1.requested_friends.filter(id=u2.id).exists()
            and u2.requested_friends.filter(id=u1.id).exists()
        ):
            u1.requested_friends.remove(u2)
            u2.requested_friends.remove(u1)
            u1.friends.add(u2)

            notification1 = Notification(
                user=u1,
                title="You got a new friend.",
                content=f"{u2.username.title()} became your friend. Let's chat!",
                link=f"/accounts/public-users#{u2.id}",
            )
            add_notification(notification1)
            notification2 = Notification(
                user=u2,
                title="You got a new friend.",
                content=f"{u1.username.title()} became your friend. Let's chat!",
                link=f"/accounts/public-users#{u1.id}",
            )
            add_notification(notification2)
        else:
            notification = Notification(
                user=u2,
                title="You have new friend request.",
                content=f"{u1.username.title()} has sent you a friend request. Let's check it!",
                link=f"/accounts/public-users#{u1.id}",
            )
            add_notification(notification)

    user = request.user
    new_friend = USER.objects.filter(id=friend_id).first()
    if (
        not user.friends.filter(id=new_friend.id).exists()
        and not user.requested_friends.filter(id=new_friend.id).exists()
    ):
        user.requested_friends.add(new_friend)
        check(user, new_friend)
    return redirect(reverse("accounts:public_users"))
