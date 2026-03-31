"""
OCP - Open-Closed Principle
Notifier: sends a message via one or more NotificationChannels.

The Notifier class is *closed for modification* – it never needs to change
when a new channel (SMS, Push, Slack, …) is introduced.  It is *open for
extension* because new channels can be injected at runtime.
"""
from src.ocp.notification_channel import NotificationChannel


class Notifier:
    """
    Dispatches notifications through a configurable set of channels.

    Follows the Strategy pattern: each channel is an interchangeable
    strategy injected at construction time.
    """

    def __init__(self, channels: list[NotificationChannel] | None = None) -> None:
        self._channels: list[NotificationChannel] = channels or []

    def add_channel(self, channel: NotificationChannel) -> None:
        self._channels.append(channel)

    def notify(self, recipient: str, message: str) -> None:
        for channel in self._channels:
            channel.send(recipient, message)
