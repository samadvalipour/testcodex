"""Permission utilities for access control."""

from rest_framework.exceptions import PermissionDenied

from . import models

# Available permission codenames:
# - can_add_permission
# - can_change_permission
# - can_delete_permission
# - can_view_permission
# - can_add_role
# - can_change_role
# - can_delete_role
# - can_view_role
# - can_assign_permission_to_role
# - can_remove_permission_from_role
# - can_assign_role_to_user
# - can_remove_role_from_user


def user_has_permission(*, user, codename):
    """Return True if the user has the specified permission codename."""
    return models.Permission.objects.filter(
        codename=codename,
        roles__userrole__user=user,
    ).exists()


def require_permission(user, codename):
    """Raise PermissionDenied if the user lacks the given permission."""
    if not user_has_permission(user=user, codename=codename):
        raise PermissionDenied("Permission denied")
