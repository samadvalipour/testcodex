from django.contrib.contenttypes.models import ContentType
from actstream.models import (
    Action,
    actor_stream,
    target_stream,
    action_object_stream,
    user_stream,
)
from actstream import action

from .models import ActivityTargets, ActivitySeenStatus


def list_activity_targets():
    return ActivityTargets.objects.all()


def list_user_activities(*, user, target=None):
    qs = actor_stream(user)
    if target:
        ct = ContentType.objects.get_for_model(target)
        qs = qs.filter(target_content_type=ct, target_object_id=target.id)
    return qs


def list_object_activities(*, obj):
    return (actor_stream(obj) | target_stream(obj) | action_object_stream(obj)).distinct()


def unseen_activities_count(*, user):
    seen_ids = ActivitySeenStatus.objects.filter(user=user, seen=True).values_list('action_id', flat=True)
    return user_stream(user).exclude(id__in=seen_ids).count()


def list_unseen_activities(*, user, target=None):
    seen_ids = ActivitySeenStatus.objects.filter(user=user, seen=True).values_list('action_id', flat=True)
    qs = user_stream(user).exclude(id__in=seen_ids)
    if target:
        ct = ContentType.objects.get_for_model(target)
        qs = qs.filter(target_content_type=ct, target_object_id=target.id)
    return qs


def list_seen_activities(*, user, target=None):
    seen_ids = ActivitySeenStatus.objects.filter(user=user, seen=True).values_list('action_id', flat=True)
    qs = user_stream(user).filter(id__in=seen_ids)
    if target:
        ct = ContentType.objects.get_for_model(target)
        qs = qs.filter(target_content_type=ct, target_object_id=target.id)
    return qs


def list_followed_targets_for_user(*, user):
    """Return the targets that the user is following."""
    return action.following(user)
