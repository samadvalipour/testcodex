from .models import Profile


def create_profile(*, user, first_name='', last_name='', bio='', avatar=''):
    profile = Profile.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        bio=bio,
        avatar=avatar,
    )
    return profile


def update_profile(*, profile, first_name=None, last_name=None, bio=None, avatar=None):
    if first_name is not None:
        profile.first_name = first_name
    if last_name is not None:
        profile.last_name = last_name
    if bio is not None:
        profile.bio = bio
    if avatar is not None:
        profile.avatar = avatar
    profile.save()
    return profile


