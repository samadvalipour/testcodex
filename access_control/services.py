from django.shortcuts import get_object_or_404

from . import models


# Permission CRUD

def create_permission(*, codename, name):
    permission = models.Permission.objects.create(codename=codename, name=name)
    return permission


def update_permission(*, permission, codename=None, name=None):
    if codename is not None:
        permission.codename = codename
    if name is not None:
        permission.name = name
    permission.save()
    return permission


def delete_permission(*, permission):
    permission.delete()


# Role CRUD

def create_role(*, name):
    role = models.Role.objects.create(name=name)
    return role


def update_role(*, role, name=None):
    if name is not None:
        role.name = name
    role.save()
    return role


def delete_role(*, role):
    role.delete()


# Assignments

def assign_permission_to_role(*, role, permission):
    role.permissions.add(permission)


def remove_permission_from_role(*, role, permission):
    role.permissions.remove(permission)


def assign_role_to_user(*, role, user):
    models.UserRole.objects.get_or_create(role=role, user=user)


def remove_role_from_user(*, role, user):
    models.UserRole.objects.filter(role=role, user=user).delete()
