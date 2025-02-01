"""
Module for managing invoice repository abstractions.
"""

from abc import ABC, abstractmethod
from typing import List
from hotel_management_system.core.domains.invoice import InvoiceIn, Invoice


class IInvoiceRepository(ABC):
    """
    Abstract base class defining the interface for an invoice repository.
    """

    @abstractmethod
    async def get_all_invoices(self) -> List[Invoice]:
        """
        Retrieve all invoices from the data storage.

        Returns:
            List[Invoice]: A list of all invoices.
        """

    @abstractmethod
    async def get_by_id(self, invoice_id: int) -> Invoice | None:
        """
        Retrieve an invoice by its unique ID.

        Args:
            invoice_id (int): The ID of the invoice.

        Returns:
            Invoice | None: The details of the invoice if found, or None if not found.
        """

    @abstractmethod
    async def add_invoice(self, data: InvoiceIn) -> Invoice | None:
        """
        Add a new invoice to the data storage.

        Args:
            data (InvoiceIn): The details of the new invoice.

        Returns:
            Invoice | None: The newly added invoice, or None if the operation fails.
        """

    @abstractmethod
    async def update_invoice(self, invoice_id: int, data: InvoiceIn) -> Invoice | None:
        """
        Update an existing invoice's data in the data storage.

        Args:
            invoice_id (int): The ID of the invoice to update.
            data (InvoiceIn): The updated details for the invoice.

        Returns:
            Invoice | None: The updated invoice details, or None if the invoice is not found.
        """

    @abstractmethod
    async def delete_invoice(self, invoice_id: int) -> bool:
        """
        Remove an invoice from the data storage.

        Args:
            invoice_id (int): The ID of the invoice to remove.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
