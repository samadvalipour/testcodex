from rest_framework import status
from rest_framework.test import APITestCase

from .factories import create_profile


class ProfileAPITests(APITestCase):

    def test_get_profile_detail(self):
        profile = create_profile()
        response = self.client.get(f'/profiles/{profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], profile.id)

    def test_update_profile(self):
        profile = create_profile()
        data = {
            'first_name': 'New',
            'last_name': 'Name',
            'bio': 'updated'
        }
        response = self.client.put(f'/profiles/{profile.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile.refresh_from_db()
        self.assertEqual(profile.first_name, 'New')
        self.assertEqual(profile.last_name, 'Name')
        self.assertEqual(profile.bio, 'updated')

