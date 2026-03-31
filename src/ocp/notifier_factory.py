"""
OCP - Open-Closed Principle
NotifierFactory: Factory that creates NotificationChannel instances by name.

Adding a new channel only requires registering it in the factory – no
existing channel code is modified.
"""
from src.ocp.notification_channel import NotificationChannel
from src.ocp.email_notifier import EmailNotifier
from src.ocp.sms_notifier import SMSNotifier
from src.ocp.push_notifier import PushNotifier
from src.ocp.slack_notifier import SlackNotifier

_REGISTRY: dict[str, type[NotificationChannel]] = {
    "email": EmailNotifier,
    "sms": SMSNotifier,
    "push": PushNotifier,
    "slack": SlackNotifier,
}


class NotifierFactory:
    """Creates NotificationChannel instances by channel name."""

    @staticmethod
    def create(channel_name: str) -> NotificationChannel:
        channel_cls = _REGISTRY.get(channel_name.lower())
        if channel_cls is None:
            raise ValueError(
                f"Unknown notification channel: '{channel_name}'. "
                f"Available: {sorted(_REGISTRY)}."
            )
        return channel_cls()

    @staticmethod
    def register(channel_name: str, channel_cls: type[NotificationChannel]) -> None:
        """Register a new channel type without modifying existing code."""
        _REGISTRY[channel_name.lower()] = channel_cls
