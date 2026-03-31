"""
Tests for SRP (Single Responsibility Principle) implementation.
Each class is tested in isolation to confirm it has a single, focused responsibility.
"""
import pytest

from src.srp.customer_validator import CustomerValidator
from src.srp.inventory_manager import InventoryManager
from src.srp.notification_service import NotificationService
from src.srp.order_processor import OrderProcessor
from src.srp.payment_processor import (
    CreditCardGateway,
    PayPalGateway,
    PaymentProcessor,
)


# ---------------------------------------------------------------------------
# CustomerValidator
# ---------------------------------------------------------------------------

class TestCustomerValidator:
    def setup_method(self):
        self.validator = CustomerValidator()

    def test_valid_customer_passes(self):
        assert self.validator.validate({"name": "Alice", "email": "alice@example.com"})

    def test_missing_name_raises(self):
        with pytest.raises(ValueError, match="name"):
            self.validator.validate({"name": "", "email": "alice@example.com"})

    def test_invalid_email_raises(self):
        with pytest.raises(ValueError, match="email"):
            self.validator.validate({"name": "Alice", "email": "not-an-email"})

    def test_missing_email_raises(self):
        with pytest.raises(ValueError, match="email"):
            self.validator.validate({"name": "Alice", "email": ""})


# ---------------------------------------------------------------------------
# PaymentProcessor
# ---------------------------------------------------------------------------

class TestCreditCardGateway:
    def setup_method(self):
        self.processor = PaymentProcessor(CreditCardGateway())

    def test_valid_charge_succeeds(self):
        assert self.processor.process(100.0, {"card_number": "4111111111111111"})

    def test_invalid_card_raises(self):
        with pytest.raises(ValueError, match="card"):
            self.processor.process(100.0, {"card_number": "123"})

    def test_zero_amount_raises(self):
        with pytest.raises(ValueError, match="amount"):
            self.processor.process(0, {"card_number": "4111111111111111"})


class TestPayPalGateway:
    def setup_method(self):
        self.processor = PaymentProcessor(PayPalGateway())

    def test_valid_paypal_charge_succeeds(self):
        assert self.processor.process(50.0, {"paypal_email": "buyer@paypal.com"})

    def test_invalid_paypal_email_raises(self):
        with pytest.raises(ValueError, match="PayPal"):
            self.processor.process(50.0, {"paypal_email": "not-an-email"})


# ---------------------------------------------------------------------------
# InventoryManager
# ---------------------------------------------------------------------------

class TestInventoryManager:
    def setup_method(self):
        self.inventory = InventoryManager()
        self.inventory.set_stock("PROD-1", 10)

    def test_reserve_reduces_stock(self):
        self.inventory.reserve("PROD-1", 3)
        assert self.inventory.get_stock("PROD-1") == 7

    def test_reserve_all_stock(self):
        self.inventory.reserve("PROD-1", 10)
        assert self.inventory.get_stock("PROD-1") == 0

    def test_insufficient_stock_raises(self):
        with pytest.raises(ValueError, match="Insufficient"):
            self.inventory.reserve("PROD-1", 11)

    def test_unknown_product_raises(self):
        with pytest.raises(ValueError, match="Insufficient"):
            self.inventory.reserve("UNKNOWN", 1)


# ---------------------------------------------------------------------------
# NotificationService
# ---------------------------------------------------------------------------

class TestNotificationService:
    def setup_method(self):
        self.service = NotificationService()

    def test_confirmation_email_is_recorded(self):
        customer = {"name": "Bob", "email": "bob@example.com"}
        self.service.send_order_confirmation(customer, "ORD-42")
        msgs = self.service.get_sent_messages()
        assert len(msgs) == 1
        assert msgs[0]["to"] == "bob@example.com"
        assert "ORD-42" in msgs[0]["subject"]

    def test_multiple_confirmations(self):
        customer = {"name": "Carol", "email": "carol@example.com"}
        self.service.send_order_confirmation(customer, "ORD-1")
        self.service.send_order_confirmation(customer, "ORD-2")
        assert len(self.service.get_sent_messages()) == 2


# ---------------------------------------------------------------------------
# OrderProcessor (integration of all SRP classes)
# ---------------------------------------------------------------------------

class TestOrderProcessor:
    def setup_method(self):
        self.validator = CustomerValidator()
        self.inventory = InventoryManager()
        self.inventory.set_stock("PROD-X", 5)
        self.payment = PaymentProcessor(CreditCardGateway())
        self.notifications = NotificationService()
        self.processor = OrderProcessor(
            self.validator, self.payment, self.inventory, self.notifications
        )
        self.customer = {"name": "Dave", "email": "dave@example.com"}
        self.payment_details = {"card_number": "4111111111111111"}

    def test_successful_order_returns_id(self):
        order_id = self.processor.place_order(
            self.customer, "PROD-X", 2, 200.0, self.payment_details
        )
        assert order_id  # non-empty string

    def test_order_reduces_inventory(self):
        self.processor.place_order(
            self.customer, "PROD-X", 3, 300.0, self.payment_details
        )
        assert self.inventory.get_stock("PROD-X") == 2

    def test_order_sends_notification(self):
        self.processor.place_order(
            self.customer, "PROD-X", 1, 100.0, self.payment_details
        )
        assert len(self.notifications.get_sent_messages()) == 1

    def test_invalid_customer_aborts_order(self):
        with pytest.raises(ValueError):
            self.processor.place_order(
                {"name": "", "email": "dave@example.com"},
                "PROD-X", 1, 100.0, self.payment_details
            )

    def test_insufficient_stock_aborts_payment(self):
        with pytest.raises(ValueError, match="Insufficient"):
            self.processor.place_order(
                self.customer, "PROD-X", 99, 100.0, self.payment_details
            )
        # Payment should NOT have been attempted (no side-effects beyond inventory)
        assert len(self.notifications.get_sent_messages()) == 0
