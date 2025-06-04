from django.test import TestCase

from access_control import services
from access_control.models import Permission, Role, UserRole
from .factories import create_permission, create_role, create_user


class AccessControlServicesTests(TestCase):
    def test_assign_role_to_user(self):
        user = create_user()
        role = create_role()
        services.assign_role_to_user(role=role, user=user)
        self.assertTrue(UserRole.objects.filter(user=user, role=role).exists())

    def test_assign_permission_to_role(self):
        role = create_role()
        permission = create_permission()
        services.assign_permission_to_role(role=role, permission=permission)
        self.assertTrue(role.permissions.filter(pk=permission.pk).exists())

