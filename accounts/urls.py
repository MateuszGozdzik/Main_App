from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm


app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),
    path(
        "reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"
    ),
]
