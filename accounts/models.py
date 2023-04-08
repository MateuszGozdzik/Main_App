from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    gravatar_link = models.URLField(null=True)
    quote_newsletter = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
