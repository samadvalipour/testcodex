from actstream import action
from actstream.models import (
    Action,
    actor_stream,
    target_stream,
    action_object_stream,
    user_stream,
)

from .models import ActivitySeenStatus


def create_activity(*, actor, verb, target=None, action_object=None):
    """Record a new activity using django-activity-stream."""
    action.send(actor, verb=verb, target=target, action_object=action_object)


def follow_target(*, user, target):
    action.follow(user, target)


def unfollow_target(*, user, target):
    action.unfollow(user, target)


def mark_activity_seen(*, user, action_obj):
    obj, _ = ActivitySeenStatus.objects.get_or_create(user=user, action=action_obj)
    obj.seen = True
    obj.save()
    return obj


def get_unseen_activities_count(*, user):
    return ActivitySeenStatus.objects.filter(user=user, seen=False).count()


def get_object_activities(*, obj):
    """Return actions related to the given object using actstream helpers."""
    return (actor_stream(obj) | target_stream(obj) | action_object_stream(obj)).distinct()


def get_user_activities(*, user):
    """Return actions performed by the given user."""
    return actor_stream(user)


def is_user_following(*, user, target):
    """Check if a user follows the given target."""
    return action.is_following(user, target)


def followers_for(*, obj):
    """Return all followers of the given object."""
    return action.followers(obj)


def following_for(*, user):
    """Return objects the user is following."""
    return action.following(user)
