from abc import ABC, abstractmethod


class INotificationService(ABC):
    @abstractmethod
    def send_otp_email(self, email: str, otp: str) -> None: ...

    @abstractmethod
    def send_activation_email(self, email: str, token: str) -> None: ...
