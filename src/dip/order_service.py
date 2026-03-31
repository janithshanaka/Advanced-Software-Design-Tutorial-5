"""
DIP - Dependency Inversion Principle
OrderService: high-level module that depends on the ILogger abstraction,
NOT on any concrete logger implementation.

The concrete logger (File / Database / Cloud) is injected at the call site
(constructor injection), so OrderService never needs to change when the
logging backend changes.
"""
from src.dip.logger import ILogger


class OrderService:
    """
    Processes orders and records activity via an injected ILogger.

    Dependency on ILogger (abstraction) rather than FileLogger (concrete)
    satisfies the Dependency Inversion Principle:
      * High-level policy (order processing) is decoupled from low-level
        detail (how logs are persisted).
      * Both the high-level module and the low-level modules depend on the
        same abstraction (ILogger).
    """

    def __init__(self, logger: ILogger) -> None:
        self._logger = logger

    def process_order(self, order_id: str, customer: str, amount: float) -> dict:
        """Process an order and return an order summary dict."""
        if amount <= 0:
            raise ValueError("Order amount must be positive.")

        self._logger.log(f"Processing order {order_id} for customer '{customer}'.")

        summary = {
            "order_id": order_id,
            "customer": customer,
            "amount": amount,
            "status": "processed",
        }

        self._logger.log(f"Order {order_id} processed successfully.")
        return summary

    def cancel_order(self, order_id: str) -> None:
        """Cancel an order."""
        self._logger.log(f"Order {order_id} cancelled.")
