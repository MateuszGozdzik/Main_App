from django.urls import path
from . import views


app_name = "pushups"

urlpatterns = [
    path("", views.index, name="index"),
]

