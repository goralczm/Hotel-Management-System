"""A module containing invoice management endpoints."""

from typing import List
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
    """
    Create a new invoice.

    Args:
        invoice (InvoiceIn): The invoice data to be added.
        invoice_service (IInvoiceService, optional): The service for managing invoice data.

    Returns:
        dict: The details of the newly created invoice.

    Raises:
        HTTPException: 400 if the invoice creation fails.
    """
    new_invoice = await invoice_service.add_invoice(invoice)
    return new_invoice.model_dump() if new_invoice else {}


@router.get("/all", response_model=List[Invoice], status_code=200)
@inject
async def get_all_invoices(
        invoice_service: IInvoiceService = Depends(Provide[Container.invoice_service]),
) -> List:
    """
    Retrieve all invoices.

    Args:
        invoice_service (IInvoiceService, optional): The service for fetching all invoice data.

    Returns:
        List: A collection of all invoices.
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
    """
    Retrieve an invoice by its ID.

    Args:
        invoice_id (int): The ID of the invoice to retrieve.
        invoice_service (IInvoiceService, optional): The service for fetching invoice data.

    Returns:
        dict | None: The invoice details if found, or None if not found.

    Raises:
        HTTPException: 404 if the invoice does not exist.
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
    """
    Update invoice data.

    Args:
        invoice_id (int): The ID of the invoice to update.
        updated_invoice (InvoiceIn): The updated invoice details.
        invoice_service (IInvoiceService, optional): The service for updating invoice data.

    Raises:
        HTTPException: 404 if the invoice does not exist.

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
    """
    Delete an invoice.

    Args:
        invoice_id (int): The ID of the invoice to delete.
        invoice_service (IInvoiceService, optional): The service for managing invoice data.

    Raises:
        HTTPException: 404 if the invoice does not exist.
    """
    if not await invoice_service.get_by_id(invoice_id=invoice_id):
        raise HTTPException(status_code=404, detail="Invoice not found")

    await invoice_service.delete_invoice(invoice_id)

    return
