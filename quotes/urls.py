from django.urls import path
from . import views


app_name = "quotes"

urlpatterns = [
    path("", views.index, name="index"),
    path("add-quote", views.add_quote, name="add_quote"),
    path("display-quote/<int:quote_id>", views.display_quote, name="display_quote"),
]

