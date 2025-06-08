from django.conf import settings
from django.db import models
from actstream.models import Action


class ActivityTargets(models.Model):
    class Titles(models.TextChoices):
        USER = 'user', 'user'
        GOAL = 'goal', 'goal'
        BADGE = 'badge', 'badge'
        POINT = 'point', 'point'
        ACHIEVEMENT = 'achievement', 'achievement'
        MISSION = 'mission', 'mission'

    title = models.CharField(max_length=20, choices=Titles.choices)

    def __str__(self):
        return self.title


class ActivitySeenStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'action')
