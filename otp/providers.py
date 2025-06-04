from abc import ABC, abstractmethod


class BaseOtpProvider(ABC):
    @abstractmethod
    def send_otp(self, phone: str, code: str) -> None:
        """Send the OTP code to the given phone."""


class ConsoleProvider(BaseOtpProvider):
    def send_otp(self, phone: str, code: str) -> None:
        print(f'Send OTP {code} to {phone}')


def get_provider() -> BaseOtpProvider:
    """Return the configured OTP provider. Currently returns the console provider."""
    return ConsoleProvider()
