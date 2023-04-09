from django.shortcuts import render, HttpResponse

from accounts.models import CustomUser


# Create your views here.
def index(request):
    return render(request, "core/index.html")


def test(request):
    u1 = CustomUser.objects.get(username="u1")
    u2 = CustomUser.objects.get(username="u2")

    u1.requested_friends.remove(u2)
    u2.requested_friends.remove(u1)

    u1.friends.remove(u2)
    u2.friends.remove(u1)


    return HttpResponse("Done")
