from django.urls import path
from . import views


app_name = "todo"

urlpatterns = [
    path("", views.index, name="index"),
    path("add-todo/", views.add_todo, name="add_todo"),
]
