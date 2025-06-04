from accounts.models import User


def create_user(**kwargs):
    phone = kwargs.get('phone', '09120000000')
    password = kwargs.get('password', 'pass1234')
    return User.objects.create_user(phone=phone, password=password)
