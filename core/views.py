from django.shortcuts import render, HttpResponse

from accounts.models import CustomUser

# Create your views here.
def index(request):

    return render(request, "core/index.html")



def test(request):
    # def check(u1, u2):
    #     if u1.requested_friends.filter(username=u2.username).exists() and u2.requested_friends.filter(username=u1.username).exists():
    #         u1.requested_friends.remove(u2)
    #         u2.requested_friends.remove(u1)
    #         u1.friends.add(u2)
    #     else:
    #         print("xd")
        

    # u1 = CustomUser.objects.get(username="u1")
    # u2 = CustomUser.objects.get(username="u2")

    # print(u1.friends.all())
    # print(u2.friends.all())

    
    # u1.save()
    # u2.save()
    return HttpResponse("Done")