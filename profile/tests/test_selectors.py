from django.test import TestCase

from profile import selectors
from .factories import create_profile


class ProfileSelectorsTests(TestCase):
    def test_get_profile_by_user(self):
        profile = create_profile()
        result = selectors.get_profile_by_user(user=profile.user)
        self.assertEqual(result, profile)

