from django.contrib.auth import get_user_model
from django.db import models
from tinymce import models as tinumce_models

User = model = get_user_model()


class Quote(models.Model):
    languages = (
        ("EN", "English"),
        ("PL", "Polish"),
    )

    title = models.CharField(max_length=50, unique=True, blank=True)
    content = tinumce_models.HTMLField(unique=True, blank=True)
    author = models.CharField(max_length=50, blank=True)
    language = models.CharField(max_length=2, choices=languages, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    favorites = models.ManyToManyField(User, related_name="favorite_quotes", blank=True)
    public = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
