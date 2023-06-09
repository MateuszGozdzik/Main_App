from django.urls import path
from . import views


app_name = "photos"

urlpatterns = [
    path("", views.index, name="index"),
    path("cat/", views.cat_photos, name="cat_photos"),
    path("dog/", views.dog_photos, name="dog_photos"),
    # path("simon/", views.simon_photos, name="simon_photos"),
    # path("special/", views.special_photos, name="special_photos"),
]
