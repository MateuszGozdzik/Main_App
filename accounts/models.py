from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    gravatar_link = models.URLField(null=True)
    
    def __str__(self):
        return self.username
