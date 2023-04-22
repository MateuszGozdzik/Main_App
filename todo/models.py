from django.contrib.auth import get_user_model
from django.db import models


class Todo(models.Model):
    status = (
        ("N", "Not Doing"),
        ("D", "Doing"),
        ("W", "Waiting"),
        ("P", "Preparing"),
        ("C", "Completed"),
    )

    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="todos"
    )
    added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=5, choices=status, default="N")

    def __str__(self) -> str:
        return self.title
