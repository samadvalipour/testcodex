from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from profile import services as profile_services
from activity import services as activity_services
from activity.models import ActivityTargets


class UserManager(BaseUserManager):
    """Custom user manager where phone number is the unique identifiers"""

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError(_('The Phone number must be set'))
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        profile_services.create_profile(user=user)
        target, _ = ActivityTargets.objects.get_or_create(
            title=ActivityTargets.Titles.USER
        )
        activity_services.create_activity(
            actor=user,
            verb='ثبت نام کرد',
            target=target,
            action_object=target,
        )
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        user = self.create_user(phone, password, **extra_fields)

        # Assign the admin role to newly created superusers
        from access_control import models as ac_models

        admin_role, _ = ac_models.Role.objects.get_or_create(name='admin')
        ac_models.UserRole.objects.get_or_create(user=user, role=admin_role)

        return user
