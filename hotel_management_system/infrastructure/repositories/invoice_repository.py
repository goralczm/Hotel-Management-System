"""Module containing invoice repository implementation."""

from typing import List

from asyncpg import Record  # type: ignore
from sqlalchemy import select

from hotel_management_system.core.repositories.i_invoice_repository import IInvoiceRepository
from hotel_management_system.core.domains.invoice import Invoice, InvoiceIn
from hotel_management_system.db import (
    invoices_table,
    database,
)


class InvoiceRepository(IInvoiceRepository):
    """A class representing continent DB repository."""

    async def get_all_invoices(self) -> List[Invoice]:
        """The method getting all invoices from the data storage.

        Returns:
            List[Invoice]: invoices in the data storage.
        """

        query = (
            select(invoices_table)
            .order_by(invoices_table.c.first_name.asc())
        )
        invoices = await database.fetch_all(query)

        return [Invoice.from_record(invoice) for invoice in invoices]

    async def get_by_id(self, invoice_id: int) -> Invoice | None:
        """The method getting invoice by provided id.

        Args:
            invoice_id (int): The id of the invoice.

        Returns:
            Invoice | None: The invoice details.
        """

        invoice = await self._get_by_id(invoice_id)

        return Invoice.from_record(invoice) if invoice else None

    async def add_invoice(self, data: InvoiceIn) -> Invoice | None:
        """The method adding new invoice to the data storage.

        Args:
            data (invoiceIn): The details of the new invoice.

        Returns:
            invoice: Full details of the newly added invoice.

        Returns:
            Invoice | None: The newly added invoice.
        """

        query = invoices_table.insert().values(**data.model_dump())
        new_invoice_id = await database.execute(query)

        return await self.get_by_id(new_invoice_id)

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
            Invoice | None: The updated invoice details.
        """

        if self._get_by_id(invoice_id):
            query = (
                invoices_table.update()
                .where(invoices_table.c.id == invoice_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            return await self.get_by_id(invoice_id)

        return None

    async def delete_invoice(self, invoice_id: int) -> bool:
        """The method updating removing invoice from the data storage.

        Args:
            invoice_id (int): The id of the invoice.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(invoice_id):
            query = invoices_table \
                .delete() \
                .where(invoices_table.c.id == invoice_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, invoice_id: int) -> Record | None:
        """A private method getting invoice from the DB based on its ID.

        Args:
            invoice_id (int): The ID of the invoice.

        Returns:
            Invoice | None: invoice record if exists.
        """

        query = (
            invoices_table.select()
            .where(invoices_table.c.id == invoice_id)
        )

        return await database.fetch_one(query)
