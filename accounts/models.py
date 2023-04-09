from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    gravatar_link = models.URLField(null=True)
    friends = models.ManyToManyField("self", blank=True)
    requested_friends = models.ManyToManyField("self", symmetrical=False, blank=True)
    
    def __str__(self):
        return self.username
