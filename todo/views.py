from django.shortcuts import render
from core.decorators import group_required




@group_required("todo")
def index(request):
    return render(request, "todo/index.html")