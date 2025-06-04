"""Utility functions for OTP authentication."""

import random
from django.contrib.auth import get_user_model

from .otp_storage import set_otp, get_otp, delete_otp
from .providers import BaseOtpProvider, get_provider
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password

User = get_user_model()


def _generate_code() -> str:
    """Return a random 6 digit numeric string."""
    return f"{random.randint(100000, 999999)}"


def send_otp_code(*, phone: str, provider: BaseOtpProvider | None = None) -> None:
    """Generate and send an OTP code to the given phone number."""
    code = _generate_code()
    hashed = make_password(code)
    set_otp(phone, hashed)
    provider = provider or get_provider()
    provider.send_otp(phone, code)


def verify_otp_code(*, phone: str, code: str) -> bool:
    """Validate an OTP code for the given phone number."""
    stored = get_otp(phone)
    if stored and check_password(code, stored):
        delete_otp(phone)
        return True
    return False


def login_or_register(*, phone: str) -> User:
    """Return an existing user for ``phone`` or create a new one."""
    user, created = User.objects.get_or_create(phone=phone)
    return user


def generate_tokens_for_user(*, user: User) -> dict:
    """Return JWT access and refresh tokens for the given user."""
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
