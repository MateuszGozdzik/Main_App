from .models import Notification
from os import getenv
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse


def add_notification(notification):
    notification.save()

    if notification.user.groups.filter(name="email notifications").exists():
        send_mail(
            subject="New Notification",
            message=f"You received new notification. Go Check: https://web-production-7633.up.railway.app{notification.link}",
            from_email=getenv("EMAIL"),
            recipient_list=[notification.user.email],
        )
        return True
    return False


@login_required
def index(request):
    notifications = request.user.notifications.all().order_by("-date")

    return render(
        request,
        "notifications/index.html",
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
        "notifications/notification.html",
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
    return redirect(reverse("notifications:index"))


@login_required
def delete_all_notifications(request):
    notifications = Notification.objects.filter(user=request.user).all()
    for notification in notifications:
        notification.delete()
    return redirect(reverse("notifications:index"))
