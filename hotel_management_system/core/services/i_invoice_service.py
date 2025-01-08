"""Module containing invoice service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from hotel_management_system.core.domains.invoice import Invoice, InvoiceIn


class IInvoiceService(ABC):
    """A class representing invoice repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[Invoice]:
        """The method getting all invoices from the repository.

        Returns:
            Iterable[invoiceDTO]: All invoices.
        """

    @abstractmethod
    async def get_by_id(self, invoice_id: int) -> Invoice | None:
        """The method getting invoice by provided id.

        Args:
            invoice_id (int): The id of the invoice.

        Returns:
            invoiceDTO | None: The invoice details.
        """

    @abstractmethod
    async def add_invoice(self, data: InvoiceIn) -> Invoice | None:
        """The method adding new invoice to the data storage.

        Args:
            data (invoiceIn): The details of the new invoice.

        Returns:
            invoice | None: Full details of the newly added invoice.
        """

    @abstractmethod
    async def update_invoice(
            self,
            invoice_id: int,
            data: InvoiceIn,
    ) -> Invoice | None:
        """The method updating invoice data in the data storage.

        Args:
            invoice_id (int): The id of the invoice.
            data (invoiceIn): The details of the updated invoice.

        Returns:
            invoice | None: The updated invoice details.
        """

    @abstractmethod
    async def delete_invoice(self, invoice_id: int) -> bool:
        """The method updating removing invoice from the data storage.

        Args:
            invoice_id (int): The id of the invoice.

        Returns:
            bool: Success of the operation.
        """