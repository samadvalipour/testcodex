from django.test import TestCase
from accounts.models import User
from access_control.models import Role, UserRole


class SuperuserAdminRoleTests(TestCase):
    def test_superuser_receives_admin_role(self):
        user = User.objects.create_superuser(phone='09125555555', password='pass1234')
        role = Role.objects.get(name='admin')
        self.assertTrue(UserRole.objects.filter(user=user, role=role).exists())

