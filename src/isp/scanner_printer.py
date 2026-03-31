"""
ISP - Interface Segregation Principle
ScannerPrinter: implements Printable and Scannable but NOT Faxable.

Only the capabilities this device genuinely supports are implemented –
no forced ``NotImplementedError`` stubs for fax.
"""
from src.isp.interfaces import Printable, Scannable


class ScannerPrinter(Printable, Scannable):
    """A printer/scanner combo that does not support faxing."""

    def __init__(self) -> None:
        self._print_jobs: list[str] = []
        self._scan_content = "Scanned document content"

    def print_document(self, document: str) -> None:
        self._print_jobs.append(document)

    def scan_document(self) -> str:
        return self._scan_content

    def get_print_jobs(self) -> list[str]:
        return list(self._print_jobs)
