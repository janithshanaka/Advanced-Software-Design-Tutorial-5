"""
OCP - Open-Closed Principle
NotificationChannel: the abstract interface that all notifiers implement.

New notification types (SMS, Push, Slack, …) are added by creating a new
subclass WITHOUT modifying the existing Notifier class or any already-
deployed channel implementation.
"""
from abc import ABC, abstractmethod


class NotificationChannel(ABC):
    """Strategy interface for all notification channels."""

    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        """Send *message* to *recipient* via this channel."""
