from accounts.models import User
from profile.models import Profile
from profile import services


def create_user(**kwargs):
    phone = kwargs.get('phone', '09120000000')
    password = kwargs.get('password', 'pass1234')
    return User.objects.create_user(phone=phone, password=password)


def create_profile(**kwargs):
    user = kwargs.get('user') or create_user()
    first_name = kwargs.get('first_name', 'John')
    last_name = kwargs.get('last_name', 'Doe')
    bio = kwargs.get('bio', 'bio text')
    avatar = kwargs.get('avatar', '')
    profile = user.profile
    services.update_profile(
        profile=profile,
        first_name=first_name,
        last_name=last_name,
        bio=bio,
        avatar=avatar,
    )
    return profile
