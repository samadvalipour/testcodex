from django.test import TestCase

from access_control import selectors
from access_control.permissions import user_has_permission
from .factories import create_permission, create_role, create_user
from access_control import services


class AccessControlSelectorsTests(TestCase):
    def test_list_roles_for_user(self):
        user = create_user()
        role = create_role()
        services.assign_role_to_user(role=role, user=user)
        roles = selectors.list_user_roles(user=user)
        self.assertIn(role, roles)

    def test_user_has_permission(self):
        user = create_user()
        role = create_role()
        permission = create_permission()
        services.assign_role_to_user(role=role, user=user)
        services.assign_permission_to_role(role=role, permission=permission)
        result = user_has_permission(user=user, codename=permission.codename)
        self.assertTrue(result)

