from . import models


def list_permissions():
    return models.Permission.objects.all()


def list_roles():
    return models.Role.objects.all()


def list_user_roles(*, user):
    return models.Role.objects.filter(userrole__user=user)


def list_role_permissions(*, role):
    return role.permissions.all()
