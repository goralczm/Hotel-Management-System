"""A module containing continent endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from hotel_management_system.container import Container
from hotel_management_system.core.domains.invoice import Invoice, InvoiceIn
from hotel_management_system.core.services.i_invoice_service import IInvoiceService

router = APIRouter()


@router.post("/create", response_model=Invoice, status_code=201)
@inject
async def create_invoice(
        invoice: InvoiceIn,
        invoice_service: IInvoiceService = Depends(Provide[Container.invoice_service])
) -> dict:
    """An endpoint for adding new invoice.

    Args:
        invoice (InvoiceIn): The invoice data.
        invoice_service (IInvoiceService, optional): The injected service dependency.

    Returns:
        dict: The new invoice attributes.
    """

    new_invoice = await invoice_service.add_invoice(invoice)

    return new_invoice.model_dump() if new_invoice else {}


@router.get("/all", response_model=Iterable[Invoice], status_code=200)
@inject
async def get_all_invoices(
        invoice_service: IInvoiceService = Depends(Provide[Container.invoice_service]),
) -> Iterable:
    """An endpoint for getting all invoices.

    Args:
        invoice_service (IInvoiceService, optional): The injected service dependency.

    Returns:
        Iterable: The invoice attributes collection.
    """

    invoices = await invoice_service.get_all()

    return invoices


@router.get(
    "/{invoice_id}",
    response_model=Invoice,
    status_code=200,
)
@inject
async def get_invoice_by_id(
        invoice_id: int,
        invoice_service: IInvoiceService = Depends(Provide[Container.invoice_service]),
) -> dict | None:
    """An endpoint for getting invoice by id.

    Args:
        invoice_id (int): The id of the invoice.
        invoice_service (IInvoiceService, optional): The injected service dependency.

    Returns:
        dict | None: The invoice details.
    """

    if invoice := await invoice_service.get_by_id(invoice_id):
        return invoice.model_dump()

    raise HTTPException(status_code=404, detail="Invoice not found")


@router.put("/{invoice_id}", response_model=Invoice, status_code=201)
@inject
async def update_invoice(
        invoice_id: int,
        updated_invoice: InvoiceIn,
        invoice_service: IInvoiceService = Depends(Provide[Container.invoice_service]),
) -> dict:
    """An endpoint for updating invoice data.

    Args:
        invoice_id (int): The id of the invoice.
        updated_invoice (InvoiceIn): The updated invoice details.
        invoice_service (IInvoiceService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if invoice does not exist.

    Returns:
        dict: The updated invoice details.
    """

    if await invoice_service.get_by_id(invoice_id=invoice_id):
        await invoice_service.update_invoice(
            invoice_id=invoice_id,
            data=updated_invoice,
        )
        return {**updated_invoice.model_dump(), "id": invoice_id}

    raise HTTPException(status_code=404, detail="Invoice not found")


@router.delete("/{invoice_id}", status_code=204)
@inject
async def delete_invoice(
        invoice_id: int,
        invoice_service: IInvoiceService = Depends(Provide[Container.invoice_service]),
) -> None:
    """An endpoint for deleting invoices.

    Args:
        invoice_id (int): The id of the invoice.
        invoice_service (IInvoiceService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if invoice does not exist.
    """

    if not await invoice_service.get_by_id(invoice_id=invoice_id):
        raise HTTPException(status_code=404, detail="Invoice not found")

    await invoice_service.delete_invoice(invoice_id)

    return
