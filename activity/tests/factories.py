from accounts.models import User
from activity.models import ActivityTarget
from actstream import action


def create_user(**kwargs):
    phone = kwargs.get('phone', '09120000000')
    password = kwargs.get('password', 'pass1234')
    return User.objects.create_user(phone=phone, password=password)


def create_target(**kwargs):
    title = kwargs.get('title', ActivityTarget.Titles.USER)
    return ActivityTarget.objects.create(title=title)


def create_action(*, actor, verb='did something', target=None, action_object=None):
    """Create an action using the actstream helper."""
    action.send(actor, verb, target=target, action_object=action_object)
