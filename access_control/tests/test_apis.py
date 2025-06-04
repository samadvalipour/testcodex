from rest_framework import status
from rest_framework.test import APITestCase

from .factories import create_user, create_role, create_permission
from access_control import services


class AccessControlAPITests(APITestCase):
    def setUp(self):
        self.user = create_user()
        perm = create_permission(codename='can_add_permission', name='can add')
        role = create_role()
        services.assign_permission_to_role(role=role, permission=perm)
        services.assign_role_to_user(role=role, user=self.user)
        self.client.force_authenticate(self.user)

    def test_create_permission_api(self):
        data = {'codename': 'test_perm', 'name': 'Test Permission'}
        response = self.client.post('/access-control/permissions/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['codename'], 'test_perm')

