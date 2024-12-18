"""A module containing continent endpoints."""

from typing import Iterable, List
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from hotel_management_system.container import Container
from hotel_management_system.core.domains.bill import BillIn
from hotel_management_system.core.domains.reservation import Reservation, ReservationIn
from hotel_management_system.core.domains.reservation_room import ReservationRoomIn
from hotel_management_system.core.services.i_bill_service import IBillService
from hotel_management_system.core.services.i_guest_service import IGuestService
from hotel_management_system.core.services.i_pricing_detail_service import IPricingDetailService
from hotel_management_system.core.services.i_reservation_room_service import IReservationRoomService
from hotel_management_system.core.services.i_reservation_service import IReservationService
from hotel_management_system.core.services.i_room_accessibility_option_service import IRoomAccessibilityOptionService
from hotel_management_system.core.services.i_room_service import IRoomService

router = APIRouter()


@router.post("/create_best_reservation", response_model=Reservation, status_code=201)
@inject
async def create_best_reservation(
        reservation: ReservationIn,
        number_of_rooms: int,
        room_service: IRoomService = Depends(Provide[Container.room_service]),
        guest_service: IGuestService = Depends(Provide[Container.guest_service]),
) -> dict:
    if not await guest_service.get_by_id(reservation.guest_id):
        raise HTTPException(status_code=404, detail=f"No guest with id: {reservation.guest_id}")

    free_rooms = await room_service.get_all_free_rooms()

    if number_of_rooms > len(free_rooms):
        raise HTTPException(status_code=409, detail="Not sufficient number of free rooms")

    room_ids_to_reserve = [room.id for room in free_rooms][:number_of_rooms]

    return await create_reservation(reservation, room_ids_to_reserve)


@router.post("/create", response_model=Reservation, status_code=201)
@inject
async def create_reservation(
        reservation: ReservationIn,
        room_ids: List[int],
        reservation_service: IReservationService = Depends(Provide[Container.reservation_service]),
        room_service: IRoomService = Depends(Provide[Container.room_service]),
        reservation_room_service: IReservationRoomService = Depends(Provide[Container.reservation_room_service]),
        guest_service: IGuestService = Depends(Provide[Container.guest_service]),
        bill_service: IBillService = Depends(Provide[Container.bill_service]),
        pricing_detail_service: IPricingDetailService = Depends(Provide[Container.pricing_detail_service]),
) -> dict:
    """An endpoint for adding new reservation.

    Args:
        reservation (ReservationIn): The reservation data.
        reservation_service (IReservationService, optional): The injected service dependency.

    Returns:
        dict: The new reservation attributes.
    """

    if not await guest_service.get_by_id(reservation.guest_id):
        raise HTTPException(status_code=404, detail=f"No guest with id: {reservation.guest_id}")

    for id in room_ids:
        if not await room_service.get_by_id(id):
            raise HTTPException(status_code=404, detail=f"No room with id: {id}")

        if await reservation_room_service.get_by_room_id(id):
            raise HTTPException(status_code=409, detail=f"Room with id: {id} is already reserved")

    new_reservation = await reservation_service.add_reservation(reservation)

    if new_reservation:
        for id in room_ids:
            new_reservation_room = ReservationRoomIn(reservation_id=new_reservation.id, room_id=id)
            await reservation_room_service.add_reservation_room(new_reservation_room)

    pricing_detail = await pricing_detail_service.get_by_name("Doba hotelowa")

    if not pricing_detail:
        raise HTTPException(status_code=404, detail="No pricing detail found")

    for id in room_ids:
        await bill_service.add_bill(BillIn(
            room_id=id,
            pricing_detail_id=pricing_detail.id,
            reservation_id=new_reservation.id
        ))

    return new_reservation if new_reservation else {}


@router.get("/all", response_model=Iterable[Reservation], status_code=200)
@inject
async def get_all_reservations(
        service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Iterable:
    """An endpoint for getting all reservations.

    Args:
        service (IReservationService, optional): The injected service dependency.

    Returns:
        Iterable: The reservation attributes collection.
    """

    reservations = await service.get_all()

    return reservations


@router.get(
    "/{reservation_id}",
    response_model=Reservation,
    status_code=200,
)
@inject
async def get_reservation_by_id(
        reservation_id: int,
        service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> dict | None:
    """An endpoint for getting reservation by id.

    Args:
        reservation_id (int): The id of the reservation.
        service (IReservationService, optional): The injected service dependency.

    Returns:
        dict | None: The reservation details.
    """

    if reservation := await service.get_by_id(reservation_id):
        return reservation

    raise HTTPException(status_code=404, detail="Reservation not found")


@router.put("/{reservation_id}", response_model=Reservation, status_code=201)
@inject
async def update_reservation(
        reservation_id: int,
        updated_reservation: ReservationIn,
        service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> dict:
    """An endpoint for updating reservation data.

    Args:
        reservation_id (int): The id of the reservation.
        updated_reservation (ReservationIn): The updated reservation details.
        service (IReservationtService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if reservation does not exist.

    Returns:
        dict: The updated reservation details.
    """

    if await service.get_by_id(reservation_id=reservation_id):
        await service.update_reservation(
            reservation_id=reservation_id,
            data=updated_reservation,
        )
        return {**updated_reservation, "id": reservation_id}

    raise HTTPException(status_code=404, detail="Reservation not found")


@router.delete("/{reservation_id}", status_code=204)
@inject
async def delete_reservation(
        reservation_id: int,
        reservation_service: IReservationService = Depends(Provide[Container.reservation_service]),
        reservation_room_service: IReservationRoomService = Depends(Provide[Container.reservation_room_service]),
) -> None:
    """An endpoint for deleting reservations.

    Args:
        reservation_id (int): The id of the reservation.
        reservation_service (IReservationService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if reservation does not exist.
    """

    if not await reservation_service.get_by_id(reservation_id=reservation_id):
        raise HTTPException(status_code=404, detail="Reservation not found")

    for reservation_room in await reservation_room_service.get_by_reservation_id(reservation_id):
        await reservation_room_service.delete_reservation_room(reservation_room.room_id, reservation_id)

    await reservation_service.delete_reservation(reservation_id)

    return
