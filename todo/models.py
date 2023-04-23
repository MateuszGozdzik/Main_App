from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now


class Todo(models.Model):
    status = (
        # ("N", "Not Doing"),
        ("D", "Doing"),
        # ("W", "Waiting"),
        # ("P", "Preparing"),
        ("C", "Completed"),
    )

    title = models.CharField(max_length=50)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="todos"
    )
    deadline = models.DateField(default=now)
    status = models.CharField(max_length=5, choices=status, default="D")

    def __str__(self) -> str:
        return self.title
