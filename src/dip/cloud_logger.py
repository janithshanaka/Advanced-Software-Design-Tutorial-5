"""
DIP - Dependency Inversion Principle
CloudLogger: low-level module that implements ILogger for cloud logging.

Useful in environments where a local file system is not available (e.g.,
serverless / container workloads).  OrderService is completely unaware of
this implementation detail.
"""
from src.dip.logger import ILogger


class CloudLogger(ILogger):
    """Sends log messages to a cloud logging service (simulated)."""

    def __init__(self, service_name: str = "CloudLogService") -> None:
        self._service_name = service_name
        self._messages: list[str] = []

    def log(self, message: str) -> None:
        # In a real implementation this would call a cloud SDK / HTTP endpoint.
        self._messages.append(f"[{self._service_name}] {message}")

    def get_messages(self) -> list[str]:
        return list(self._messages)
