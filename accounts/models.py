from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    gravatar_link = models.URLField(null=True)
    friends = models.ManyToManyField("self", blank=True)
    requested_friends = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __str__(self):
        return self.username


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, related_name="notifications", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    link = models.CharField()

    def __str__(self) -> str:
        return self.title
