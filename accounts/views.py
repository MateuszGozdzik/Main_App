import hashlib
import random
from os import getenv

from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse

from .forms import (
    CustomUserCreationForm,
    GravatarForm,
    ProfileSection1Form,
    ProfileSection2Form,
)
from .models import Notification

USER = get_user_model()


def add_notification(notification):
    notification.save()

    if notification.user.groups.filter(name="email notifications").exists():
        send_mail(
            subject="New Notification",
            message=f"You received new notification. Go Check: https://web-production-7633.up.railway.app{notification.link}",
            from_email=getenv("EMAIL"),
            recipient_list=[notification.user.email],
        )
        print("sent")
    return True


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
                    if (
                        public == "True"
                        and not user.groups.filter(name=group.name).exists()
                    ):
                        print("add")
                        group.user_set.add(user)
                    elif (
                        public == "False"
                        and user.groups.filter(name=group.name).exists()
                    ):
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
                    if (
                        quote_newsletter == "True"
                        and not request.user.groups.filter(name=group.name).exists()
                    ):
                        group.user_set.add(request.user)
                    elif (
                        quote_newsletter == "False"
                        and request.user.groups.filter(name=group.name).exists()
                    ):
                        group.user_set.remove(request.user)
                    return redirect(reverse("accounts:profile"))
                else:
                    return HttpResponse("Error: Group not found")
        else:
            form = ProfileSection2Form()
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


@login_required
def notification_view(request):
    notifications = request.user.notifications.all().order_by("-date")

    return render(
        request,
        "accounts/notifications.html",
        {
            "notifications": notifications,
        },
    )


@login_required
def notification_detail(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    if notification.user != request.user:
        return render(
            request,
            "core/index.html",
            {
                "error": "This wasn't your notification!",
            },
        )
    if notification.read == False:
        notification.read = True
        notification.save()
    return render(
        request,
        "accounts/notification_details.html",
        {
            "notification": notification,
        },
    )


@login_required
def delete_notification(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    if notification.user != request.user:
        return render(
            request,
            "core/index.html",
            {
                "error": "This wasn't your notification!",
            },
        )
    notification.delete()
    return redirect(reverse("accounts:notifications"))
