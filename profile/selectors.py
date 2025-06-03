from .models import Profile


def get_profile_by_user(*, user):
    return Profile.objects.filter(user=user).first()

