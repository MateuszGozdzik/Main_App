from django.shortcuts import render, redirect
from django.urls import reverse
from core.decorators import group_required
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q


@group_required("todo")
def index(request):
    class DayTodos:
        def __init__(self, date, todos: list) -> None:
            self.date = date
            self.day_of_week = date.strftime("%A")
            self.todos = todos

    def get_todos(user, day, yesterday=False):
        if yesterday:
            todos = Todo.objects.filter(
                Q(user=user, deadline=day) | Q(user=user, deadline__lt=day, status="D")
            ).order_by("status")
        else:
            todos = Todo.objects.filter(user=user, deadline=day).order_by("status")
        return DayTodos(day, todos)

    today = timezone.now().date()
    todos = [
        get_todos(request.user, day)
        for day in [today + timedelta(days=i) for i in range(4)]
    ]
    yesterday = today - timedelta(days=1)
    todos.insert(0, get_todos(request.user, yesterday, yesterday=True))

    return render(
        request,
        "todo/index.html",
        {
            "todos": todos,
        },
    )


@group_required("todo")
def add_todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect(reverse("todo:index"))
    else:
        form = TodoForm()

    return render(request, "todo/add_todo.html", {"form": form})


# @group_required("todo")
# def delete_todo(request, todo_id):
#     todo = Todo.objects.get(id=todo_id)
#     if todo.user == request.user:
#         todo.delete()
#     return redirect(reverse("todo:index"))


# @group_required("todo")
# def todo_details(request, todo_id):
#     todo = Todo.objects.get(id=todo_id)
#     return render(request, "todo/todo_details.html", {"todo": todo})
