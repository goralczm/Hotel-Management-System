"""Module containing continent service implementation."""

from typing import Iterable

from hotel_management_system.core.domains.invoice import Invoice, InvoiceIn
from hotel_management_system.core.repositories.i_invoice_repository import IInvoiceRepository
from hotel_management_system.core.services.i_invoice_service import IInvoiceService
from hotel_management_system.core.services.i_reservation_service import IReservationService


class InvoiceService(IInvoiceService):
    """A class implementing the invoice service."""

    _invoice_repository: IInvoiceRepository
    _reservation_service: IReservationService

    def __init__(self,
                 invoice_repository: IInvoiceRepository,
                 reservation_service: IReservationService,
                 ) -> None:
        """The initializer of the `invoice service`.

        Args:
            repository (IinvoiceRepository): The reference to the repository.
        """

        self._invoice_repository = invoice_repository
        self._reservation_service = reservation_service

    async def get_all(self) -> Iterable[Invoice]:
        """The method getting all invoices from the repository.

        Returns:
            Iterable[invoiceDTO]: All invoices.
        """

        all_invoices = await self._invoice_repository.get_all_invoices()

        return [await self.parse_invoice(invoice) for invoice in all_invoices]

    async def get_by_id(self, invoice_id: int) -> Invoice | None:
        """The method getting invoice by provided id.

        Args:
            invoice_id (int): The id of the invoice.

        Returns:
            invoiceDTO | None: The invoice details.
        """

        return await self.parse_invoice(
            await self._invoice_repository.get_by_id(invoice_id)
        )

    async def add_invoice(self, data: InvoiceIn) -> Invoice | None:
        """The method adding new invoice to the data storage.

        Args:
            data (invoiceIn): The details of the new invoice.

        Returns:
            invoice | None: Full details of the newly added invoice.
        """

        return await self.parse_invoice(
            await self._invoice_repository.add_invoice(data)
        )

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

        return await self.parse_invoice(
            await self._invoice_repository.update_invoice(
                invoice_id=invoice_id,
                data=data,
            )
        )

    async def delete_invoice(self, invoice_id: int) -> bool:
        """The method updating removing invoice from the data storage.

        Args:
            invoice_id (int): The id of the invoice.

        Returns:
            bool: Success of the operation.
        """

        return await self._invoice_repository.delete_invoice(invoice_id)

    async def parse_invoice(self, invoice: Invoice) -> Invoice:
        if invoice:
            reservation = await self._reservation_service.get_by_id(invoice.reservation_id)

            invoice.reservation = reservation
            invoice.total_sum = reservation.get_cost()

        return invoice
