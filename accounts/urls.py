from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, PasswordResetView
from .forms import LoginForm


app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),
    path("reset_password/", PasswordResetView.as_view(), name="reset_password"),
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path(
        "update_profile/<int:section_id>", views.update_profile, name="update_profile"
    ),
    path("change-gravatar/", views.change_gravatar, name="change_gravatar"),
    path("public-users", views.public_users, name="public_users"),
    path(
        "friend_request/<int:friend_id>",
        views.send_friend_request,
        name="friend_request",
    ),
    path("notifications/", views.notification_view, name="notifications"),
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
]
