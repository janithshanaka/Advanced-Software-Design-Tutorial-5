"""
SRP - Single Responsibility Principle
OrderProcessor: orchestrates the order workflow by delegating each
responsibility to the appropriate single-purpose class.

Before refactoring, this 2000-line class handled:
  - Customer validation
  - Credit-card and PayPal payment processing
  - Inventory updates
  - Email notifications

After applying SRP each concern lives in its own class:
  - CustomerValidator    -> validates customer data
  - PaymentProcessor     -> charges via a pluggable PaymentGateway
  - InventoryManager     -> manages stock levels
  - NotificationService  -> sends email confirmations

Benefits:
  * Each class has a single reason to change.
  * Payment-gateway changes no longer risk breaking notification logic.
  * Classes can be tested in isolation.
  * New gateways / notification channels can be added without touching
    unrelated code.
"""
import uuid

from src.srp.customer_validator import CustomerValidator
from src.srp.inventory_manager import InventoryManager
from src.srp.notification_service import NotificationService
from src.srp.payment_processor import PaymentProcessor


class OrderProcessor:
    """
    Thin orchestrator that coordinates the order workflow.

    Its only responsibility is *coordination* – it owns no business logic
    of its own and delegates every sub-task to a specialised collaborator.
    """

    def __init__(
        self,
        validator: CustomerValidator,
        payment_processor: PaymentProcessor,
        inventory_manager: InventoryManager,
        notification_service: NotificationService,
    ) -> None:
        self._validator = validator
        self._payment_processor = payment_processor
        self._inventory_manager = inventory_manager
        self._notification_service = notification_service

    def place_order(
        self,
        customer: dict,
        product_id: str,
        quantity: int,
        amount: float,
        payment_details: dict,
    ) -> str:
        """
        Execute the full order workflow and return the new order ID.

        Raises ValueError if any validation or processing step fails.
        """
        self._validator.validate(customer)
        self._inventory_manager.reserve(product_id, quantity)
        self._payment_processor.process(amount, payment_details)

        order_id = str(uuid.uuid4())
        self._notification_service.send_order_confirmation(customer, order_id)
        return order_id
