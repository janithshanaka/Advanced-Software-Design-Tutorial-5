"""
DIP - Dependency Inversion Principle
ILogger: the high-level abstraction that both OrderService and concrete
logger implementations depend upon.

Before refactoring: OrderService imported FileLogger directly.
  from file_logger import FileLogger          # concrete, low-level detail
  class OrderService:
      def __init__(self):
          self._logger = FileLogger()          # hard dependency

After refactoring: OrderService depends only on ILogger (abstraction).
  class OrderService:
      def __init__(self, logger: ILogger):     # injected abstraction
          self._logger = logger

Benefits:
  * OrderService is never modified when the logging backend changes.
  * FileLogger, DatabaseLogger, CloudLogger all satisfy the same contract.
  * Unit tests can inject a lightweight in-memory logger.
"""
from abc import ABC, abstractmethod


class ILogger(ABC):
    """Abstraction for all logging backends."""

    @abstractmethod
    def log(self, message: str) -> None:
        """Write *message* to the logging backend."""
