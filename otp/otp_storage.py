import redis
from django.conf import settings


REDIS_URL = settings.REDIS_URL
OTP_EXPIRATION_SECONDS = settings.OTP_EXPIRATION_SECONDS

redis_client = redis.Redis.from_url(REDIS_URL)


def set_otp(phone: str, code: str) -> None:
    redis_client.setex(f'otp:{phone}', OTP_EXPIRATION_SECONDS, code)


def get_otp(phone: str) -> str | None:
    value = redis_client.get(f'otp:{phone}')
    if value:
        return value.decode()
    return None


def delete_otp(phone: str) -> None:
    redis_client.delete(f'otp:{phone}')
