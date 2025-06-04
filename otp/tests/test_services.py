from django.test import TestCase
from unittest.mock import patch

from otp import services
from otp.otp_storage import redis_client


class OtpServiceTests(TestCase):
    def setUp(self):
        redis_client.flushdb()

    def test_send_and_verify_otp(self):
        with patch('otp.providers.get_provider') as get_provider, \
             patch('otp.services._generate_code', return_value='123456'):
            get_provider.return_value.send_otp.return_value = None
            services.send_otp_code(phone='09120000000')
            stored_hash = redis_client.get('otp:09120000000')
            self.assertIsNotNone(stored_hash)
            self.assertNotEqual(stored_hash.decode(), '123456')
            from django.contrib.auth.hashers import check_password
            self.assertTrue(check_password('123456', stored_hash.decode()))
        result = services.verify_otp_code(phone='09120000000', code='123456')
        self.assertTrue(result)
        self.assertIsNone(redis_client.get('otp:09120000000'))

    def test_generate_tokens(self):
        user = services.login_or_register(phone='09120000001')
        tokens = services.generate_tokens_for_user(user=user)
        self.assertIn('access', tokens)
        self.assertIn('refresh', tokens)
