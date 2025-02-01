"""
Module containing invoice service implementation.
"""

from typing import Iterable

from hotel_management_system.core.domains.invoice import Invoice, InvoiceIn
from hotel_management_system.core.repositories.i_invoice_repository import IInvoiceRepository
from hotel_management_system.core.services.i_invoice_service import IInvoiceService
from hotel_management_system.core.services.i_reservation_service import IReservationService


class InvoiceService(IInvoiceService):
    """
    A class implementing the invoice service.
    """

    _invoice_repository: IInvoiceRepository
    _reservation_service: IReservationService

    def __init__(self,
                 invoice_repository: IInvoiceRepository,
                 reservation_service: IReservationService,
                 ) -> None:
        """
        The initializer of the `invoice service`.

        Args:
            invoice_repository (IInvoiceRepository): The reference to the invoice repository
            reservation_service (IReservationService): The reference to the reservation service
        """

        self._invoice_repository = invoice_repository
        self._reservation_service = reservation_service

    async def get_all(self) -> Iterable[Invoice]:
        """
        Retrieve all invoices from the data storage.

        Returns:
            List[Invoice]: A list of all invoices.
        """

        all_invoices = await self._invoice_repository.get_all_invoices()

        return [await self.parse_invoice(invoice) for invoice in all_invoices]

    async def get_by_id(self, invoice_id: int) -> Invoice | None:
        """
        Retrieve an invoice by its unique ID.

        Args:
            invoice_id (int): The ID of the invoice.

        Returns:
            Invoice | None: The details of the invoice if found, or None if not found.
        """

        return await self.parse_invoice(
            await self._invoice_repository.get_by_id(invoice_id)
        )

    async def add_invoice(self, data: InvoiceIn) -> Invoice | None:
        """
        Add a new invoice to the data storage.

        Args:
            data (InvoiceIn): The details of the new invoice.

        Returns:
            Invoice | None: The newly added invoice, or None if the operation fails.
        """

        return await self.parse_invoice(
            await self._invoice_repository.add_invoice(data)
        )

    async def update_invoice(
            self,
            invoice_id: int,
            data: InvoiceIn,
    ) -> Invoice | None:
        """
        Update an existing invoice's data in the data storage.

        Args:
            invoice_id (int): The ID of the invoice to update.
            data (InvoiceIn): The updated details for the invoice.

        Returns:
            Invoice | None: The updated invoice details, or None if the invoice is not found.
        """

        return await self.parse_invoice(
            await self._invoice_repository.update_invoice(
                invoice_id=invoice_id,
                data=data,
            )
        )

    async def delete_invoice(self, invoice_id: int) -> bool:
        """
        Remove an invoice from the data storage.

        Args:
            invoice_id (int): The ID of the invoice to remove.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """

        return await self._invoice_repository.delete_invoice(invoice_id)

    async def parse_invoice(self, invoice: Invoice) -> Invoice:
        if invoice:
            reservation = await self._reservation_service.get_by_id(invoice.reservation_id)

            invoice.reservation = reservation
            invoice.total_sum = reservation.get_cost()

        return invoice
