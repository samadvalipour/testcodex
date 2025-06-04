from django.shortcuts import get_object_or_404

"""Helper functions for managing permissions and roles."""

from . import models


# Permission CRUD

def create_permission(*, codename, name):
    """Create a new permission with the given codename and name."""
    permission = models.Permission.objects.create(codename=codename, name=name)
    return permission


def update_permission(*, permission, codename=None, name=None):
    """Update fields of ``permission`` and return it."""
    if codename is not None:
        permission.codename = codename
    if name is not None:
        permission.name = name
    permission.save()
    return permission


def delete_permission(*, permission):
    """Remove the given permission from the database."""
    permission.delete()


# Role CRUD

def create_role(*, name):
    """Create a new role with the given name."""
    role = models.Role.objects.create(name=name)
    return role


def update_role(*, role, name=None):
    """Update ``role`` with a new ``name`` if provided."""
    if name is not None:
        role.name = name
    role.save()
    return role


def delete_role(*, role):
    """Delete the given role from the database."""
    role.delete()


# Assignments

def assign_permission_to_role(*, role, permission):
    """Attach a permission to a role."""
    role.permissions.add(permission)


def remove_permission_from_role(*, role, permission):
    """Detach a permission from a role."""
    role.permissions.remove(permission)


def assign_role_to_user(*, role, user):
    """Assign ``role`` to ``user``."""
    models.UserRole.objects.get_or_create(role=role, user=user)


def remove_role_from_user(*, role, user):
    """Remove ``role`` from ``user``."""
    models.UserRole.objects.filter(role=role, user=user).delete()
