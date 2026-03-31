"""
SRP - Single Responsibility Principle
NotificationService: responsible only for sending email notifications.
"""


class NotificationService:
    """Sends email notifications to customers."""

    def __init__(self) -> None:
        self._sent: list[dict] = []

    def send_order_confirmation(self, customer: dict, order_id: str) -> None:
        """Send an order-confirmation email to the customer."""
        message = {
            "to": customer["email"],
            "subject": f"Order Confirmation - {order_id}",
            "body": f"Dear {customer['name']}, your order {order_id} has been confirmed.",
        }
        self._sent.append(message)

    def get_sent_messages(self) -> list[dict]:
        return list(self._sent)
