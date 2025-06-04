from django.test import TestCase
from accounts.models import User
from activity.models import ActivityTargets
from actstream.models import Action


class UserActivityTests(TestCase):
    def test_activity_created_for_new_user(self):
        user = User.objects.create_user(phone='09124444444', password='pass1234')
        target = ActivityTargets.objects.get(title=ActivityTargets.Titles.USER)
        action = Action.objects.last()
        self.assertEqual(action.actor, user)
        self.assertEqual(action.target, target)
        self.assertEqual(action.action_object, target)
        self.assertEqual(action.verb, 'ثبت نام کرد')
