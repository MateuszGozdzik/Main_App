from django.shortcuts import render, HttpResponse

from accounts.models import CustomUser

# Create your views here.
def index(request):

    return render(request, "core/index.html")



def test(request):
    return HttpResponse("Done")