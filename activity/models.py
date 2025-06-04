from django.conf import settings
from django.db import models
from actstream.models import Action


class ActivityTarget(models.Model):
    class Titles(models.TextChoices):
        USER = 'user', 'User'
        GOAL = 'goal', 'Goal'
        BADGE = 'badge', 'Badge'
        POINT = 'point', 'Point'
        ACHIEVEMENT = 'achievement', 'Achievement'
        MISSION = 'mission', 'Mission'

    title = models.CharField(max_length=20, choices=Titles.choices)

    def __str__(self):
        return self.title


class ActivitySeenStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'action')
