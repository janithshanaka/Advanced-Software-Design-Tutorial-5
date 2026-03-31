"""
Tests for DIP (Dependency Inversion Principle) implementation.
Verifies that OrderService depends only on ILogger and works correctly
with any concrete logger injected at runtime.
"""
import os
import tempfile
import pytest

from src.dip.cloud_logger import CloudLogger
from src.dip.database_logger import DatabaseLogger
from src.dip.file_logger import FileLogger
from src.dip.logger import ILogger
from src.dip.order_service import OrderService


# ---------------------------------------------------------------------------
# ILogger contract: all loggers must satisfy the same interface
# ---------------------------------------------------------------------------

class TestILoggerContract:
    def test_database_logger_is_ilogger(self):
        assert isinstance(DatabaseLogger(), ILogger)

    def test_cloud_logger_is_ilogger(self):
        assert isinstance(CloudLogger(), ILogger)

    def test_file_logger_is_ilogger(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".log") as f:
            path = f.name
        try:
            assert isinstance(FileLogger(path), ILogger)
        finally:
            os.unlink(path)


# ---------------------------------------------------------------------------
# DatabaseLogger
# ---------------------------------------------------------------------------

class TestDatabaseLogger:
    def setup_method(self):
        self.logger = DatabaseLogger()

    def test_log_stores_record(self):
        self.logger.log("event 1")
        assert "event 1" in self.logger.get_records()

    def test_multiple_logs(self):
        self.logger.log("a")
        self.logger.log("b")
        assert len(self.logger.get_records()) == 2


# ---------------------------------------------------------------------------
# CloudLogger
# ---------------------------------------------------------------------------

class TestCloudLogger:
    def setup_method(self):
        self.logger = CloudLogger("TestService")

    def test_log_prefixes_service_name(self):
        self.logger.log("startup")
        assert self.logger.get_messages()[0].startswith("[TestService]")

    def test_multiple_messages(self):
        self.logger.log("x")
        self.logger.log("y")
        assert len(self.logger.get_messages()) == 2


# ---------------------------------------------------------------------------
# FileLogger
# ---------------------------------------------------------------------------

class TestFileLogger:
    def test_log_writes_to_file(self):
        with tempfile.NamedTemporaryFile(
            mode="r", delete=False, suffix=".log"
        ) as f:
            path = f.name
        try:
            logger = FileLogger(path)
            logger.log("file log entry")
            with open(path, encoding="utf-8") as fh:
                content = fh.read()
            assert "file log entry" in content
        finally:
            os.unlink(path)

    def test_multiple_writes_append(self):
        with tempfile.NamedTemporaryFile(
            mode="r", delete=False, suffix=".log"
        ) as f:
            path = f.name
        try:
            logger = FileLogger(path)
            logger.log("line1")
            logger.log("line2")
            with open(path, encoding="utf-8") as fh:
                lines = fh.readlines()
            assert len(lines) == 2
        finally:
            os.unlink(path)


# ---------------------------------------------------------------------------
# OrderService – DIP: works with any ILogger implementation
# ---------------------------------------------------------------------------

class TestOrderServiceWithDatabaseLogger:
    def setup_method(self):
        self.logger = DatabaseLogger()
        self.service = OrderService(self.logger)

    def test_process_order_returns_summary(self):
        result = self.service.process_order("ORD-001", "Alice", 150.0)
        assert result["order_id"] == "ORD-001"
        assert result["status"] == "processed"

    def test_process_order_logs_activity(self):
        self.service.process_order("ORD-002", "Bob", 75.0)
        records = self.logger.get_records()
        assert any("ORD-002" in r for r in records)

    def test_cancel_order_logs(self):
        self.service.cancel_order("ORD-003")
        assert any("ORD-003" in r for r in self.logger.get_records())

    def test_negative_amount_raises(self):
        with pytest.raises(ValueError, match="positive"):
            self.service.process_order("ORD-X", "Eve", -10)


class TestOrderServiceWithCloudLogger:
    def setup_method(self):
        self.logger = CloudLogger("ProdCloud")
        self.service = OrderService(self.logger)

    def test_process_order_logs_to_cloud(self):
        self.service.process_order("ORD-100", "Charlie", 200.0)
        messages = self.logger.get_messages()
        assert any("ORD-100" in m for m in messages)


class TestDIPSubstitution:
    """
    Demonstrates that OrderService works identically regardless of which
    concrete ILogger is injected – the essence of DIP.
    """

    def _run_with_logger(self, logger: ILogger) -> None:
        service = OrderService(logger)
        result = service.process_order("ORD-999", "Tester", 1.0)
        assert result["status"] == "processed"

    def test_works_with_database_logger(self):
        self._run_with_logger(DatabaseLogger())

    def test_works_with_cloud_logger(self):
        self._run_with_logger(CloudLogger())

    def test_works_with_custom_in_memory_logger(self):
        """A lightweight test double satisfying ILogger."""
        class InMemoryLogger(ILogger):
            def __init__(self):
                self.logs = []
            def log(self, message: str) -> None:
                self.logs.append(message)

        logger = InMemoryLogger()
        self._run_with_logger(logger)
        assert len(logger.logs) > 0
