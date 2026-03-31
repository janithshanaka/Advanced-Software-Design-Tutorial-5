"""
Tests for ISP (Interface Segregation Principle) implementation.
Verifies that each printer class only implements the interfaces it
genuinely supports, and that clients can code against minimal interfaces.
"""
import pytest

from src.isp.all_in_one_printer import AllInOnePrinter
from src.isp.basic_printer import BasicPrinter
from src.isp.interfaces import Faxable, Printable, Scannable
from src.isp.scanner_printer import ScannerPrinter


# ---------------------------------------------------------------------------
# BasicPrinter – only Printable
# ---------------------------------------------------------------------------

class TestBasicPrinter:
    def setup_method(self):
        self.printer = BasicPrinter()

    def test_implements_printable(self):
        assert isinstance(self.printer, Printable)

    def test_does_not_implement_scannable(self):
        assert not isinstance(self.printer, Scannable)

    def test_does_not_implement_faxable(self):
        assert not isinstance(self.printer, Faxable)

    def test_print_document_records_job(self):
        self.printer.print_document("Report.pdf")
        assert "Report.pdf" in self.printer.get_print_jobs()

    def test_multiple_print_jobs(self):
        self.printer.print_document("Doc1")
        self.printer.print_document("Doc2")
        assert len(self.printer.get_print_jobs()) == 2


# ---------------------------------------------------------------------------
# ScannerPrinter – Printable + Scannable, NOT Faxable
# ---------------------------------------------------------------------------

class TestScannerPrinter:
    def setup_method(self):
        self.printer = ScannerPrinter()

    def test_implements_printable(self):
        assert isinstance(self.printer, Printable)

    def test_implements_scannable(self):
        assert isinstance(self.printer, Scannable)

    def test_does_not_implement_faxable(self):
        assert not isinstance(self.printer, Faxable)

    def test_print_and_scan(self):
        self.printer.print_document("Invoice.pdf")
        scanned = self.printer.scan_document()
        assert "Invoice.pdf" in self.printer.get_print_jobs()
        assert scanned  # non-empty content


# ---------------------------------------------------------------------------
# AllInOnePrinter – Printable + Scannable + Faxable
# ---------------------------------------------------------------------------

class TestAllInOnePrinter:
    def setup_method(self):
        self.printer = AllInOnePrinter()

    def test_implements_all_interfaces(self):
        assert isinstance(self.printer, Printable)
        assert isinstance(self.printer, Scannable)
        assert isinstance(self.printer, Faxable)

    def test_print_document(self):
        self.printer.print_document("Contract.pdf")
        assert "Contract.pdf" in self.printer.get_print_jobs()

    def test_scan_document(self):
        content = self.printer.scan_document()
        assert content

    def test_fax_document(self):
        self.printer.fax_document("Proposal.pdf", "+1-800-000-0000")
        faxes = self.printer.get_fax_jobs()
        assert len(faxes) == 1
        assert faxes[0]["recipient"] == "+1-800-000-0000"


# ---------------------------------------------------------------------------
# ISP client code: depends only on the interface it needs
# ---------------------------------------------------------------------------

class TestISPClientCode:
    def test_printable_client_accepts_any_printer(self):
        """A function that only needs Printable works with all printer types."""
        def do_print(device: Printable, doc: str) -> None:
            device.print_document(doc)

        for printer in [BasicPrinter(), ScannerPrinter(), AllInOnePrinter()]:
            do_print(printer, "Test")

    def test_scannable_client_rejects_basic_printer(self):
        """A function needing Scannable should not receive a BasicPrinter."""
        basic = BasicPrinter()
        assert not isinstance(basic, Scannable)
