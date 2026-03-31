"""
Tests for OCP (Open-Closed Principle) implementation.
Verifies that new notification channels can be added without modifying
existing Notifier or channel implementations.
"""
import pytest

from src.ocp.email_notifier import EmailNotifier
from src.ocp.notifier import Notifier
from src.ocp.notifier_factory import NotifierFactory
from src.ocp.notification_channel import NotificationChannel
from src.ocp.push_notifier import PushNotifier
from src.ocp.slack_notifier import SlackNotifier
from src.ocp.sms_notifier import SMSNotifier


# ---------------------------------------------------------------------------
# Individual channel tests
# ---------------------------------------------------------------------------

class TestEmailNotifier:
    def test_send_records_message(self):
        notifier = EmailNotifier()
        notifier.send("alice@example.com", "Hello!")
        sent = notifier.get_sent()
        assert len(sent) == 1
        assert sent[0]["channel"] == "email"
        assert sent[0]["to"] == "alice@example.com"


class TestSMSNotifier:
    def test_send_records_message(self):
        notifier = SMSNotifier()
        notifier.send("+1-555-0100", "Your code is 1234")
        sent = notifier.get_sent()
        assert sent[0]["channel"] == "sms"


class TestPushNotifier:
    def test_send_records_message(self):
        notifier = PushNotifier()
        notifier.send("device-token-xyz", "New message!")
        assert notifier.get_sent()[0]["channel"] == "push"


class TestSlackNotifier:
    def test_send_records_message(self):
        notifier = SlackNotifier()
        notifier.send("#general", "Deployment complete")
        assert notifier.get_sent()[0]["channel"] == "slack"


# ---------------------------------------------------------------------------
# Notifier (multi-channel dispatcher)
# ---------------------------------------------------------------------------

class TestNotifier:
    def test_dispatches_to_all_channels(self):
        email = EmailNotifier()
        sms = SMSNotifier()
        notifier = Notifier([email, sms])
        notifier.notify("recipient", "Test message")
        assert len(email.get_sent()) == 1
        assert len(sms.get_sent()) == 1

    def test_add_channel_dynamically(self):
        notifier = Notifier()
        push = PushNotifier()
        notifier.add_channel(push)
        notifier.notify("device", "Push alert")
        assert len(push.get_sent()) == 1

    def test_empty_channels_does_nothing(self):
        notifier = Notifier()
        notifier.notify("nobody", "silence")  # should not raise


# ---------------------------------------------------------------------------
# NotifierFactory
# ---------------------------------------------------------------------------

class TestNotifierFactory:
    def test_create_email(self):
        channel = NotifierFactory.create("email")
        assert isinstance(channel, EmailNotifier)

    def test_create_sms(self):
        assert isinstance(NotifierFactory.create("sms"), SMSNotifier)

    def test_create_push(self):
        assert isinstance(NotifierFactory.create("push"), PushNotifier)

    def test_create_slack(self):
        assert isinstance(NotifierFactory.create("slack"), SlackNotifier)

    def test_unknown_channel_raises(self):
        with pytest.raises(ValueError, match="Unknown"):
            NotifierFactory.create("fax")

    def test_register_new_channel_without_modifying_existing_code(self):
        """
        OCP in action: adding a new channel only requires registering it;
        no existing class is modified.
        """
        class TelegramNotifier(NotificationChannel):
            def send(self, recipient: str, message: str) -> None:
                pass  # pragma: no cover

        NotifierFactory.register("telegram", TelegramNotifier)
        channel = NotifierFactory.create("telegram")
        assert isinstance(channel, TelegramNotifier)
