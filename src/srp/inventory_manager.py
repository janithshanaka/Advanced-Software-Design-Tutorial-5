"""
SRP - Single Responsibility Principle
InventoryManager: responsible only for updating product inventory.
"""


class InventoryManager:
    """Manages stock levels for products."""

    def __init__(self) -> None:
        self._stock: dict[str, int] = {}

    def set_stock(self, product_id: str, quantity: int) -> None:
        self._stock[product_id] = quantity

    def reserve(self, product_id: str, quantity: int) -> bool:
        """Reserve *quantity* units of *product_id*. Returns True on success."""
        available = self._stock.get(product_id, 0)
        if available < quantity:
            raise ValueError(
                f"Insufficient stock for product '{product_id}': "
                f"requested {quantity}, available {available}."
            )
        self._stock[product_id] = available - quantity
        return True

    def get_stock(self, product_id: str) -> int:
        return self._stock.get(product_id, 0)
