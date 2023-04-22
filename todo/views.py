from django.shortcuts import render, redirect
from django.urls import reverse
from core.decorators import group_required
from .forms import TodoForm
from .models import Todo
from django.utils import timezone


@group_required("todo")
def index(request):
    today = timezone.now().date()
    todays_todos = Todo.objects.filter(user=request.user, deadline__lte=today)
    return render(
        request,
        "todo/index.html",
        {
            "todays_todos": todays_todos,
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
