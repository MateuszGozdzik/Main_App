from django.urls import path
from . import views


app_name = "todo"

urlpatterns = [
    path("", views.index, name="index"),
    path("add-todo/", views.add_todo, name="add_todo"),
    # path("delete-todo/<int:todo_id>/", views.delete_todo, name="delete_todo"),
    # path("<int:todo_id>/", views.todo_details, name="todo_details"),
]
