"""
DIP - Dependency Inversion Principle
DatabaseLogger: low-level module that implements ILogger for database logging.

Switching from FileLogger to DatabaseLogger requires *zero* changes to
OrderService – only the injected dependency at composition-root changes.
"""
from src.dip.logger import ILogger


class DatabaseLogger(ILogger):
    """Stores log messages in an in-memory database (simulated)."""

    def __init__(self) -> None:
        self._records: list[str] = []

    def log(self, message: str) -> None:
        self._records.append(message)

    def get_records(self) -> list[str]:
        return list(self._records)
