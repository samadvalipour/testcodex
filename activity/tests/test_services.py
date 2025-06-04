from django.test import TestCase
from actstream.models import Action

from activity import services
from .factories import create_user, create_target, create_action


class ActivityServiceTests(TestCase):
    def test_follow_unfollow(self):
        user = create_user()
        target = create_target()
        services.follow_target(user=user, target=target)
        from actstream.models import Follow
        self.assertTrue(Follow.objects.filter(user=user, target_object_id=target.id).exists())
        services.unfollow_target(user=user, target=target)
        self.assertFalse(Follow.objects.filter(user=user, target_object_id=target.id).exists())

    def test_mark_activity_seen(self):
        user = create_user()
        target = create_target()
        create_action(actor=user, target=target)
        action_obj = Action.objects.first()
        services.mark_activity_seen(user=user, action_obj=action_obj)
        from activity.models import ActivitySeenStatus
        self.assertTrue(ActivitySeenStatus.objects.filter(user=user, action=action_obj, seen=True).exists())

    def test_get_object_activities(self):
        user = create_user()
        target = create_target()
        create_action(actor=user, target=target)
        actions = services.get_object_activities(obj=target)
        self.assertEqual(actions.count(), 1)

    def test_get_user_activities(self):
        user = create_user()
        create_action(actor=user)
        actions = services.get_user_activities(user=user)
        self.assertEqual(actions.count(), 1)
