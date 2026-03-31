"""
DIP - Dependency Inversion Principle
FileLogger: low-level module that implements ILogger for file-based logging.

In the original design OrderService depended directly on this class.
After DIP refactoring, FileLogger depends on ILogger (the abstraction) –
it no longer *owns* the OrderService relationship.
"""
import os

from src.dip.logger import ILogger


class FileLogger(ILogger):
    """Writes log messages to a file."""

    def __init__(self, filepath: str) -> None:
        self._filepath = filepath

    def log(self, message: str) -> None:
        with open(self._filepath, "a", encoding="utf-8") as fh:
            fh.write(message + "\n")
