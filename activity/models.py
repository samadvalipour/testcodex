from django.conf import settings
from django.db import models
from actstream.models import Action


class ActivityTargets(models.Model):
    class Titles(models.TextChoices):
        USER = 'user', 'کاربر'
        GOAL = 'goal', 'هدف'
        BADGE = 'badge', 'نشان'
        POINT = 'point', 'امتیاز'
        ACHIEVEMENT = 'achievement', 'دستاورد'
        MISSION = 'mission', 'ماموریت'

    title = models.CharField(max_length=20, choices=Titles.choices)

    def __str__(self):
        return self.title


class ActivitySeenStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'action')
