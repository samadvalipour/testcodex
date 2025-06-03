from django.test import TestCase

from profile import services
from accounts.models import User
from .factories import create_profile


class ProfileServicesTests(TestCase):
    def test_create_profile(self):
        user = User.objects.create(phone='09120000001')
        profile = services.create_profile(
            user=user,
            first_name='Jane',
            last_name='Smith',
            bio='hello'
        )
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.first_name, 'Jane')
        self.assertEqual(profile.last_name, 'Smith')
        self.assertEqual(profile.bio, 'hello')

    def test_update_profile(self):
        profile = create_profile()
        services.update_profile(profile=profile, first_name='New', last_name='Name', bio='new bio')
        profile.refresh_from_db()
        self.assertEqual(profile.first_name, 'New')
        self.assertEqual(profile.last_name, 'Name')
        self.assertEqual(profile.bio, 'new bio')

