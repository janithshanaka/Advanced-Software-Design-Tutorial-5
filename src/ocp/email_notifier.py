"""
OCP - Open-Closed Principle
EmailNotifier: concrete NotificationChannel for email delivery.
"""
from src.ocp.notification_channel import NotificationChannel


class EmailNotifier(NotificationChannel):
    """Sends notifications via email."""

    def __init__(self) -> None:
        self._sent: list[dict] = []

    def send(self, recipient: str, message: str) -> None:
        record = {"channel": "email", "to": recipient, "message": message}
        self._sent.append(record)

    def get_sent(self) -> list[dict]:
        return list(self._sent)
