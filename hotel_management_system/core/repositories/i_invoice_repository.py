"""Module containing invoice repository abstractions."""

from abc import ABC, abstractmethod
from typing import List

from hotel_management_system.core.domains.invoice import InvoiceIn, Invoice


class IInvoiceRepository(ABC):
    """An abstract class representing protocol of continent repository."""

    @abstractmethod
    async def get_all_invoices(self) -> List[Invoice]:
        """The abstract getting all invoices from the data storage.

        Returns:
            List[Invoice]: Invoices in the data storage.
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
        """The abstract adding new invoice to the data storage.

        Args:
            data (InvoiceIn): The details of the new invoice.

        Returns:
            Invoice | None: The newly added invoice.
        """

    @abstractmethod
    async def update_invoice(
            self,
            invoice_id: int,
            data: InvoiceIn,
    ) -> Invoice | None:
        """The abstract updating invoice data in the data storage.

        Args:
            invoice_id (int): The id of the invoice.
            data (InvoiceIn): The details of the updated invoice.

        Returns:
            Invoice | None: The updated invoice details.
        """

    @abstractmethod
    async def delete_invoice(self, invoice_id: int) -> bool:
        """The abstract updating removing invoice from the data storage.

        Args:
            invoice_id (int): The id of the invoice.

        Returns:
            bool: Success of the operation.
        """