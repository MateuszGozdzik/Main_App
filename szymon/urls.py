from django.urls import path
from . import views


app_name = "szymon"

urlpatterns = [
    path("", views.index, name="index"),
]

