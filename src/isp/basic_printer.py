"""
ISP - Interface Segregation Principle
BasicPrinter: implements only the Printable interface.

Clients that only need to print can depend solely on ``Printable``; they
are not burdened by scan or fax dependencies.
"""
from src.isp.interfaces import Printable


class BasicPrinter(Printable):
    """A simple printer that only supports printing."""

    def __init__(self) -> None:
        self._jobs: list[str] = []

    def print_document(self, document: str) -> None:
        self._jobs.append(document)

    def get_print_jobs(self) -> list[str]:
        return list(self._jobs)
