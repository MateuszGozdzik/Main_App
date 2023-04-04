from django.db import models
from accounts.models import CustomUser

# Create your models here.
class PushUp(models.Model):
    PUSHUP_CHOICES = (
        ("NR", "Normal"),
        ("WD", "Wide"),
        ("DM", "Diamond"),
        ("EX", "Explosive"),
        ("SS", "Side to Side"),
        ("CP", "Clapping"),
        ("AR", "Archer"),
        ("OC", "Open Close"),
        ("TW", "TypeWriter"),
        ("ST", "Shoulder Tap")
    )
    name = models.CharField(max_length=2, choices=PUSHUP_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    reps = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)