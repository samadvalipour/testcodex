from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from accounts.models import User


class OtpAPITests(APITestCase):
    def test_send_and_verify_flow(self):
        with patch('otp.providers.get_provider') as get_provider, \
             patch('otp.services._generate_code', return_value='123456'):
            get_provider.return_value.send_otp.return_value = None
            response = self.client.post('/otp/', {'phone': '09120000000'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            from otp.otp_storage import redis_client
            stored = redis_client.get('otp:09120000000')
            self.assertIsNotNone(stored)
            self.assertNotEqual(stored.decode(), '123456')
            from django.contrib.auth.hashers import check_password
            self.assertTrue(check_password('123456', stored.decode()))
            response = self.client.post('/otp/', {'phone': '09120000000', 'code': '123456'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(User.objects.filter(phone='09120000000').exists())
            self.assertIn('access', response.data)
            self.assertIn('refresh', response.data)
            self.assertIsNone(redis_client.get('otp:09120000000'))

