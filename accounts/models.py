from django.db import models
from django.contrib.auth.models import AbstractUser
import hashlib
import random


class CustomUser(AbstractUser):

    gravatar_link = models.URLField()

    def save(self, *args, **kwargs):
        hash = hashlib.md5(
            str(random.getrandbits(128)).encode('utf-8')).hexdigest()
        self.gravatar_link = f"https://www.gravatar.com/avatar/{hash}?d=identicon"

        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
