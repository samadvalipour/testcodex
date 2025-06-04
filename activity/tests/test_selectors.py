from django.test import TestCase

from activity import selectors
from .factories import create_user, create_target, create_action


class ActivitySelectorTests(TestCase):
    def test_list_activity_targets(self):
        target = create_target()
        targets = selectors.list_activity_targets()
        self.assertIn(target, targets)

    def test_unseen_count(self):
        user = create_user()
        target = create_target()
        from activity import services
        services.follow_target(user=user, target=target)
        create_action(actor=user, target=target)
        count = selectors.unseen_activities_count(user=user)
        self.assertEqual(count, 1)
        from activity.models import ActivitySeenStatus
        from actstream.models import Action
        action_obj = Action.objects.first()
        ActivitySeenStatus.objects.create(user=user, action=action_obj, seen=True)
        count = selectors.unseen_activities_count(user=user)
        self.assertEqual(count, 0)

    def test_object_and_user_activities(self):
        user = create_user()
        create_action(actor=user)
        actions = selectors.list_user_activities(user=user)
        self.assertEqual(actions.count(), 1)
        obj_actions = selectors.list_object_activities(obj=user)
        self.assertEqual(obj_actions.count(), 1)

    def test_list_followed_targets_for_user(self):
        user = create_user()
        target = create_target()
        from activity import services
        services.follow_target(user=user, target=target)
        followed = selectors.list_followed_targets_for_user(user=user)
        self.assertIn(target, list(followed))
