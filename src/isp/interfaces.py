"""
ISP - Interface Segregation Principle
Segregated printer interfaces.

Before refactoring: a single fat ``Printer`` interface forced every
implementor to provide ``print()``, ``scan()``, and ``fax()`` even when
they only needed printing.  Classes that only printed had to raise
``NotImplementedError`` for scan/fax – a classic ISP violation.

After refactoring: three focused interfaces.
  * ``Printable``  – only ``print_document()``
  * ``Scannable``  – only ``scan_document()``
  * ``Faxable``    – only ``fax_document()``

Clients depend only on the interface(s) they actually use, and concrete
classes implement only the capabilities they genuinely support.
"""
from abc import ABC, abstractmethod


class Printable(ABC):
    """Capability interface for devices that can print."""

    @abstractmethod
    def print_document(self, document: str) -> None:
        """Send *document* to the printer."""


class Scannable(ABC):
    """Capability interface for devices that can scan."""

    @abstractmethod
    def scan_document(self) -> str:
        """Scan a physical document and return its content."""


class Faxable(ABC):
    """Capability interface for devices that can fax."""

    @abstractmethod
    def fax_document(self, document: str, recipient_fax: str) -> None:
        """Fax *document* to *recipient_fax*."""
