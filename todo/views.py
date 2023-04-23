from django.shortcuts import render, redirect
from django.urls import reverse
from core.decorators import group_required
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from datetime import timedelta


@group_required("todo")
def index(request):
    def get_todos(user, day):
        return Todo.objects.filter(user=user, deadline=day).order_by("status")

    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    post_tomorrow = today + timedelta(days=2)

    yesterday_todos = Todo.objects.filter(user=request.user, deadline__lte=yesterday).order_by("-status")
    today_todos = get_todos(request.user, today)
    tomorrow_todos = get_todos(request.user, tomorrow)
    post_tomorrow_todos = get_todos(request.user, post_tomorrow)

    todos = {
        yesterday: yesterday_todos,
        today: today_todos,
        tomorrow: tomorrow_todos,
        post_tomorrow: post_tomorrow_todos,
    }
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
