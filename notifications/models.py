from django.db import models
from django.contrib.auth import get_user_model


class Notification(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="notifications", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    link = models.CharField()
    read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
