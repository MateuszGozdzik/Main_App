from django.urls import path
from . import views


app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("test/", views.test, name="test"),
    path("health/", views.health, name="health"),
]
