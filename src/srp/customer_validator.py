"""
SRP - Single Responsibility Principle
CustomerValidator: responsible only for validating customer data.
"""


class CustomerValidator:
    """Validates customer information before order processing."""

    def validate(self, customer: dict) -> bool:
        """Return True if the customer data is valid, False otherwise."""
        if not customer.get("name"):
            raise ValueError("Customer name is required.")
        if not customer.get("email") or "@" not in customer["email"]:
            raise ValueError("A valid customer email is required.")
        return True
