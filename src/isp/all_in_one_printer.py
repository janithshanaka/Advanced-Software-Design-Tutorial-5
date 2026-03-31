"""
ISP - Interface Segregation Principle
AllInOnePrinter: implements Printable, Scannable, AND Faxable.

Only devices that truly support all three capabilities implement all
three interfaces.  This is correct ISP usage: no forced stubs.
"""
from src.isp.interfaces import Faxable, Printable, Scannable


class AllInOnePrinter(Printable, Scannable, Faxable):
    """A full-featured printer/scanner/fax machine."""

    def __init__(self) -> None:
        self._print_jobs: list[str] = []
        self._fax_jobs: list[dict] = []
        self._scan_content = "Scanned document content"

    def print_document(self, document: str) -> None:
        self._print_jobs.append(document)

    def scan_document(self) -> str:
        return self._scan_content

    def fax_document(self, document: str, recipient_fax: str) -> None:
        self._fax_jobs.append({"document": document, "recipient": recipient_fax})

    def get_print_jobs(self) -> list[str]:
        return list(self._print_jobs)

    def get_fax_jobs(self) -> list[dict]:
        return list(self._fax_jobs)
