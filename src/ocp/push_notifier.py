"""
OCP - Open-Closed Principle
PushNotifier: concrete NotificationChannel for mobile push notifications.
"""
from src.ocp.notification_channel import NotificationChannel


class PushNotifier(NotificationChannel):
    """Sends mobile push notifications."""

    def __init__(self) -> None:
        self._sent: list[dict] = []

    def send(self, recipient: str, message: str) -> None:
        record = {"channel": "push", "to": recipient, "message": message}
        self._sent.append(record)

    def get_sent(self) -> list[dict]:
        return list(self._sent)
