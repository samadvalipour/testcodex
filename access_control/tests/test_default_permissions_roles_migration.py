from django.test import TestCase
from access_control.models import Role, Permission


class DefaultPermissionsRolesMigrationTests(TestCase):
    def test_admin_role_has_all_permissions(self):
        admin_role = Role.objects.get(name='admin')
        all_perms = set(Permission.objects.values_list('codename', flat=True))
        admin_perms = set(admin_role.permissions.values_list('codename', flat=True))
        self.assertEqual(admin_perms, all_perms)
