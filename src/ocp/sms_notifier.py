"""
OCP - Open-Closed Principle
SMSNotifier: concrete NotificationChannel for SMS delivery.

Adding this class does not require any modification to existing code.
"""
from src.ocp.notification_channel import NotificationChannel


class SMSNotifier(NotificationChannel):
    """Sends notifications via SMS."""

    def __init__(self) -> None:
        self._sent: list[dict] = []

    def send(self, recipient: str, message: str) -> None:
        record = {"channel": "sms", "to": recipient, "message": message}
        self._sent.append(record)

    def get_sent(self) -> list[dict]:
        return list(self._sent)
