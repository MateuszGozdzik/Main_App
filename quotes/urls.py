from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.index, name="index"),
    path("add-quote", views.add_quote, name="add_quote"),
    path("update-quote/<int:quote_id>", views.update_quote, name="update_quote"),
    path("display-quote/<int:quote_id>", views.index, name="display_quote"),
    path("favorite/<int:quote_id>", views.favorite_quote, name="favorite_quote"),
    path(
        "admin/approve-quotes", views.approve_quotes_panel, name="approve_quotes_panel"
    ),
    path(
        "admin/approve-quote/<int:quote_id>",
        views.approve_quote_panel,
        name="approve_quote_panel",
    ),
    path(
        "admin/approve-quote/<int:quote_id>/<str:decision>",
        views.approve_quote,
        name="approve_quote",
    ),
]
