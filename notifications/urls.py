from django.urls import path
from . import views


app_name = "notifications"


urlpatterns = [
    path("", views.index, name="index"),
    path(
        "notification/<int:notification_id>",
        views.notification_detail,
        name="notification_detail",
    ),
    path(
        "delete_notification/<int:notification_id>",
        views.delete_notification,
        name="delete_notification",
    ),
    path(
        "delete-notifications/",
        views.delete_all_notifications,
        name="delete_notifications",
    ),
]
