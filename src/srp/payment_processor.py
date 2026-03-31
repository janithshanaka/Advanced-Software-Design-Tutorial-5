"""
SRP - Single Responsibility Principle
PaymentProcessor: responsible only for processing payments via different gateways.
"""
from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    """Abstract base for payment gateways."""

    @abstractmethod
    def charge(self, amount: float, details: dict) -> bool:
        """Charge the given amount using the payment gateway."""


class CreditCardGateway(PaymentGateway):
    """Handles credit-card payment processing."""

    def charge(self, amount: float, details: dict) -> bool:
        card_number = details.get("card_number", "")
        if not card_number or len(card_number) < 13:
            raise ValueError("Invalid credit card number.")
        # Simulate successful charge
        return True


class PayPalGateway(PaymentGateway):
    """Handles PayPal payment processing."""

    def charge(self, amount: float, details: dict) -> bool:
        paypal_email = details.get("paypal_email", "")
        if not paypal_email or "@" not in paypal_email:
            raise ValueError("Invalid PayPal email.")
        # Simulate successful charge
        return True


class PaymentProcessor:
    """Processes payments by delegating to the appropriate gateway."""

    def __init__(self, gateway: PaymentGateway) -> None:
        self._gateway = gateway

    def process(self, amount: float, payment_details: dict) -> bool:
        if amount <= 0:
            raise ValueError("Payment amount must be positive.")
        return self._gateway.charge(amount, payment_details)
