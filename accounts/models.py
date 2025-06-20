from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser):
    phone = models.CharField(max_length=15, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser  
    
    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def __str__(self):
        return self.phone
