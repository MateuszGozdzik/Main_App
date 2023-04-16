from django.shortcuts import render, HttpResponse
from accounts.models import CustomUser
from quotes.models import Quote


def index(request):
    return render(request, "core/index.html")


def health(request):
    return HttpResponse("WORKING")


def test(request):
    return HttpResponse("Done")
