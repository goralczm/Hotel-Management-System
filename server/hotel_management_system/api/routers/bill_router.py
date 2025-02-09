"""A module containing bill management endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from hotel_management_system.container import Container
from hotel_management_system.core.services.i_pricing_detail_service import IPricingDetailService
from hotel_management_system.core.services.i_reservation_service import IReservationService
from hotel_management_system.core.services.i_room_service import IRoomService
from hotel_management_system.core.domains.bill import Bill, BillIn
from hotel_management_system.core.services.i_bill_service import IBillService

router = APIRouter()


@router.post("/create", response_model=Bill, status_code=201)
@inject
async def create_bill(
        bill: BillIn,
        room_service: IRoomService = Depends(Provide[Container.room_service]),
        pricing_detail_service: IPricingDetailService = Depends(Provide[Container.pricing_detail_service]),
        bill_service: IBillService = Depends(Provide[Container.bill_service]),
        reservation_service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> dict:
    """
    Create a new bill for a reservation.

    Args:
        bill (BillIn): The bill details to be created.
        room_service (IRoomService, optional): Service for room data validation.
        pricing_detail_service (IPricingDetailService, optional): Service for pricing detail validation.
        bill_service (IBillService, optional): Service for creating a new bill.
        reservation_service (IReservationService, optional): Service for reservation validation.

    Returns:
        dict: The created bill's details.

    Raises:
        HTTPException: 404 if any related data (room, pricing detail, or reservation) is not found.
    """
    if not await room_service.get_by_id(bill.room_id):
        raise HTTPException(status_code=404, detail="Room id not found")

    if not await pricing_detail_service.get_by_id(bill.pricing_detail_id):
        raise HTTPException(status_code=404, detail="Pricing detail id not found")

    if not await reservation_service.get_by_id(bill.reservation_id):
        raise HTTPException(status_code=404, detail="Reservation id not found")

    new_bill = await bill_service.add_bill(bill)
    return new_bill.model_dump() if new_bill else {}


@router.get("/all", response_model=Iterable[Bill], status_code=200)
@inject
async def get_all_bills(
        service: IBillService = Depends(Provide[Container.bill_service]),
) -> Iterable:
    """
    Retrieve all bills.

    Args:
        service (IBillService, optional): The service to fetch all bills.

    Returns:
        Iterable: A collection of all bills.
    """
    bills = await service.get_all()
    return bills


@router.get(
    "/{room_pricing_detail_id}",
    response_model=Bill,
    status_code=200,
)
@inject
async def get_bill_by_id(
        room_id: int,
        pricing_detail_id: int,
        service: IBillService = Depends(Provide[Container.bill_service]),
) -> dict | None:
    """
    Retrieve a bill by room ID and pricing detail ID.

    Args:
        room_id (int): The room ID associated with the bill.
        pricing_detail_id (int): The pricing detail ID associated with the bill.
        service (IBillService, optional): The service to fetch the bill.

    Returns:
        dict | None: The bill details if found, else None.

    Raises:
        HTTPException: 404 if the bill is not found.
    """
    if bill := await service.get_by_id(room_id, pricing_detail_id):
        return bill.model_dump()

    raise HTTPException(status_code=404, detail="Bill not found")


@router.put("/{room_pricing_detail_id}", response_model=Bill, status_code=201)
@inject
async def update_bill(
        room_id: int,
        pricing_detail_id: int,
        updated_bill: BillIn,
        service: IBillService = Depends(Provide[Container.bill_service]),
) -> dict:
    """
    Update an existing bill's details.

    Args:
        room_id (int): The room ID associated with the bill.
        pricing_detail_id (int): The pricing detail ID associated with the bill.
        updated_bill (BillIn): The updated bill details.
        service (IBillService, optional): The service to update the bill.

    Raises:
        HTTPException: 404 if the bill is not found.

    Returns:
        dict: The updated bill's details.
    """
    if await service.get_by_id(room_id=room_id, pricing_detail_id=pricing_detail_id):
        await service.update_bill(
            room_id=room_id,
            pricing_detail_id=pricing_detail_id,
            data=updated_bill,
        )
        return {**updated_bill.model_dump()}

    raise HTTPException(status_code=404, detail="Bill not found")


@router.delete("/{reservation_id}", status_code=204)
@inject
async def delete_bill_by_reservation_id(
        reservation_id: int,
        service: IBillService = Depends(Provide[Container.bill_service]),
) -> None:
    """
    Delete a bill by room ID and pricing detail ID.

    Args:
        reservation_id (int): The reservation ID associated with the bill.
        service (IBillService, optional): The service to delete the bill.

    Raises:
        HTTPException: 404 if the bill is not found.
    """
    await service.delete_bill_by_reservation_id(reservation_id)

    return
