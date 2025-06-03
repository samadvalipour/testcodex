from django.test import TestCase

from accounts.models import User
from profile.models import Profile


class UserProfileCreationTests(TestCase):
    def test_profile_created_with_user(self):
        user = User.objects.create_user(phone='09123333333', password='pass1234')
        self.assertTrue(Profile.objects.filter(user=user).exists())
