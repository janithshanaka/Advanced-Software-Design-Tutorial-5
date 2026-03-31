"""
OCP - Open-Closed Principle
SlackNotifier: concrete NotificationChannel for Slack messaging.
"""
from src.ocp.notification_channel import NotificationChannel


class SlackNotifier(NotificationChannel):
    """Sends notifications to a Slack channel."""

    def __init__(self) -> None:
        self._sent: list[dict] = []

    def send(self, recipient: str, message: str) -> None:
        record = {"channel": "slack", "to": recipient, "message": message}
        self._sent.append(record)

    def get_sent(self) -> list[dict]:
        return list(self._sent)
