from django.urls import path
from . import views


app_name = "pushups"

urlpatterns = [
    path("", views.index, name="index"),
    path("100/", views.genereate100, name="100")
]
