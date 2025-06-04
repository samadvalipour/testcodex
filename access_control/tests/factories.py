from accounts.models import User
from access_control import services


def create_user(**kwargs):
    phone = kwargs.get('phone', '09121111111')
    password = kwargs.get('password', 'pass1234')
    return User.objects.create_user(phone=phone, password=password)


def create_permission(**kwargs):
    codename = kwargs.get('codename', 'perm_' + str(services.models.Permission.objects.count()))
    name = kwargs.get('name', codename)
    return services.create_permission(codename=codename, name=name)


def create_role(**kwargs):
    name = kwargs.get('name', 'role_' + str(services.models.Role.objects.count()))
    return services.create_role(name=name)

