from django.conf import settings
from django.db import models
from django.core.validators import MaxLengthValidator


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True, validators=[MaxLengthValidator(300)])
    avatar = models.URLField(blank=True)

    def __str__(self):
        name = f'{self.first_name} {self.last_name}'.strip()
        return name or f'Profile for {self.user.phone}'
