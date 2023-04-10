from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.index, name="index"),
    path("add-quote", views.add_quote, name="add_quote"),
    path("display-quote/<int:quote_id>", views.index, name="display_quote"),
    path("favorite/<int:quote_id>", views.favorite_quote, name="favorite_quote"),
]
