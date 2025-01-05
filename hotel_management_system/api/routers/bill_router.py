"""A module containing continent endpoints."""

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
    """An endpoint for adding new bill.

    Args:
        bill (BillIn): The bill data.
        room_service (IRoomService, optional): The injected room service dependency
        pricing_detail_service (IPricingDetailService, optional): The injected pricing_detail service dependency
        bill_service (IBillService, optional): The injected service dependency.

    Returns:
        dict: The new bill attributes.
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
    """An endpoint for getting all bills.

    Args:
        service (IBillService, optional): The injected service dependency.

    Returns:
        Iterable: The bill attributes collection.
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
    """An endpoint for getting bill by id.

    Args:
        room_id (int): The id of the room
        pricing_detail_id (int): The id of the accessibility_option.
        service (IBillService, optional): The injected service dependency.

    Returns:
        dict | None: The bill details.
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
    """An endpoint for updating bill data.

    Args:
        room_id (int): The id of the room
        pricing_detail_id (int): The id of the accessibility_option.
        updated_bill (BillIn): The updated bill details.
        service (IBillService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if bill does not exist.

    Returns:
        dict: The updated bill details.
    """

    if await service.get_by_id(room_id=room_id, pricing_detail_id=pricing_detail_id):
        await service.update_bill(
            room_id=room_id,
            pricing_detail_id=pricing_detail_id,
            data=updated_bill,
        )
        return {**updated_bill.model_dump()}

    raise HTTPException(status_code=404, detail="Bill not found")


@router.delete("/{room_pricing_detail_id}", status_code=204)
@inject
async def delete_bill(
        room_id: int,
        pricing_detail_id: int,
        service: IBillService = Depends(Provide[Container.bill_service]),
) -> None:
    """An endpoint for deleting bills.

    Args:
        room_id (int): The id of the room
        pricing_detail_id (int): The id of the accessibility_option.
        service (IcontinentService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if bill does not exist.
    """

    if await service.get_by_id(room_id=room_id, pricing_detail_id=pricing_detail_id):
        await service.delete_bill(room_id, pricing_detail_id)

        return

    raise HTTPException(status_code=404, detail="Bill not found")
