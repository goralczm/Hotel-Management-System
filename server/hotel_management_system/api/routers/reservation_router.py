"""A module containing reservation endpoints."""

from datetime import date
from typing import Iterable, List
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from hotel_management_system.container import Container
from hotel_management_system.core.domains.bill import BillIn
from hotel_management_system.core.domains.reservation import Reservation, ReservationIn
from hotel_management_system.core.domains.reservation_room import ReservationRoomIn
from hotel_management_system.core.domains.room import Room
from hotel_management_system.core.services.i_accessibility_option_service import IAccessibilityOptionService
from hotel_management_system.core.services.i_bill_service import IBillService
from hotel_management_system.core.services.i_guest_service import IGuestService
from hotel_management_system.core.services.i_pricing_detail_service import IPricingDetailService
from hotel_management_system.core.services.i_reservation_room_service import IReservationRoomService
from hotel_management_system.core.services.i_reservation_service import IReservationService
from hotel_management_system.core.services.i_room_service import IRoomService

router = APIRouter()


@router.post("/create_best_reservation", response_model=Reservation, status_code=201)
@inject
async def create_best_reservation(
        reservation: ReservationIn,
        number_of_rooms: int,
        additional_accessibility_option_ids: List[int] = [-1],
        accessibility_option_service: IAccessibilityOptionService =
        Depends(Provide[Container.accessibility_option_service]),
        reservation_service: IReservationService = Depends(Provide[Container.reservation_service]),
        guest_service: IGuestService = Depends(Provide[Container.guest_service]),
) -> Reservation | dict:
    """
    Create a reservation with the best available rooms based on guest preferences.

    Args:
        reservation (ReservationIn): The reservation data.
        number_of_rooms (int): The number of rooms to reserve.
        additional_accessibility_option_ids (List[int]): The list of additional accessibility option ids specific
                                                                                                    to the reservation
        accessibility_option_service (IAccessibilityOptionService, optional): The injected reservation
                                                                                        accessibility option dependency.
        reservation_service (IReservationService, optional): The injected reservation service dependency.
        guest_service (IGuestService, optional): The injected guest service dependency.

    Returns:
        Reservation | dict: The reservation details or an empty dictionary if no reservation is created.

    Raises:
        HTTPException: If the guest does not exist.
        HTTPException: If there are not enough available rooms.
        HTTPException: If the accessibility option does not exist.
    """
    if not await guest_service.get_by_id(reservation.guest_id):
        raise HTTPException(status_code=404, detail=f"No guest with id: {reservation.guest_id}")

    accessibility_options = []
    for accessibility_option_id in additional_accessibility_option_ids:
        if accessibility_option_id == -1:
            continue

        if accessibility_option := await accessibility_option_service.get_by_id(accessibility_option_id):
            accessibility_options.append(accessibility_option)
        else:
            raise HTTPException(status_code=404, detail=f"No accessibility option found")

    free_rooms = await reservation_service.get_free_rooms(reservation.start_date, reservation.end_date)

    if number_of_rooms > len(free_rooms):
        raise HTTPException(status_code=409, detail="Not enough free rooms available")

    guest = await guest_service.get_by_id(reservation.guest_id)

    existing_accessibility_option_ids = (accessibility_option.id for accessibility_option in accessibility_options)
    accessibility_options += [accessibility_option for accessibility_option in guest.accessibility_options if accessibility_option.id not in existing_accessibility_option_ids]

    sorted_rooms = []

    if len(accessibility_options) > 0:
        sorted_rooms = sorted(free_rooms,
                              key=lambda room: room.correlation_coefficient(accessibility_options),
                              reverse=True)
    else:
        sorted_rooms = sorted(free_rooms,
                              key=lambda room: len(room.accessibility_options) == 0,
                              reverse=True)

    room_ids_to_reserve = [room.id for room in sorted_rooms][:number_of_rooms]

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
) -> Reservation | dict:
    """
    Create a new reservation and assign rooms to it.

    Args:
        reservation (ReservationIn): The reservation data.
        room_ids (List[int]): The list of room IDs to reserve.
        reservation_service (IReservationService, optional): The injected reservation service dependency.
        room_service (IRoomService, optional): The injected room service dependency.
        reservation_room_service (IReservationRoomService, optional): The injected reservation room service dependency.
        guest_service (IGuestService, optional): The injected guest service dependency.
        bill_service (IBillService, optional): The injected bill service dependency.
        pricing_detail_service (IPricingDetailService, optional): The injected pricing detail service dependency.

    Returns:
        Reservation | dict: The new reservation details or an empty dictionary if the reservation was not created.

    Raises:
        HTTPException: If reservation end date is less or equal the start date.
        HTTPException: If the guest is not found
        HTTPException: If the rooms are not found
        HTTPException: If no pricing detail is found.
    """
    if reservation.end_date <= reservation.start_date:
        raise HTTPException(status_code=409, detail="Reservation end date cannot be before the start date")

    if not await guest_service.get_by_id(reservation.guest_id):
        raise HTTPException(status_code=404, detail=f"No guest with id: {reservation.guest_id}")

    for id in room_ids:
        if not await room_service.get_by_id(id):
            raise HTTPException(status_code=404, detail=f"No room with id: {id}")

    new_reservation = await reservation_service.add_reservation(reservation)

    if new_reservation:
        for id in room_ids:
            new_reservation_room = ReservationRoomIn(reservation_id=new_reservation.id, room_id=id)
            await reservation_room_service.add_reservation_room(new_reservation_room)

    pricing_detail = await pricing_detail_service.get_by_name("Doba hotelowa")

    if not pricing_detail:
        await reservation_service.delete_reservation(new_reservation.id)
        raise HTTPException(status_code=404, detail="No pricing detail found")

    for day in range(reservation.get_duration()):
        for id in room_ids:
            await bill_service.add_bill(BillIn(
                room_id=id,
                pricing_detail_id=pricing_detail.id,
                reservation_id=new_reservation.id
            ))

    new_reservation = await reservation_service.get_by_id(new_reservation.id)

    return new_reservation if new_reservation else {}


@router.get("/free_rooms", response_model=Iterable[Room], status_code=200)
@inject
async def get_all_free_rooms(
        start_date: date,
        end_date: date,
        service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Iterable:
    """
    Get all free rooms for the given date range.

    Args:
        start_date (date): The start date for the reservation period.
        end_date (date): The end date for the reservation period.
        service (IReservationService, optional): The injected reservation service dependency.

    Returns:
        Iterable[Room]: A list of free rooms.
    """
    return await service.get_free_rooms(start_date, end_date)


@router.get("/all", response_model=Iterable[Reservation], status_code=200)
@inject
async def get_all_reservations(
        service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Iterable:
    """
    Get all reservations.

    Args:
        service (IReservationService, optional): The injected reservation service dependency.

    Returns:
        Iterable[Reservation]: A collection of reservation details.
    """
    reservations = await service.get_all()

    return reservations


@router.get("/all/between_months/", response_model=Iterable[Reservation], status_code=200)
@inject
async def get_all_reservations_between_months(
        start_date: date,
        end_date: date,
        service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Iterable:
    """
    Get all reservations within a specified date range.

    Args:
        start_date (date): The start date of the date range.
        end_date (date): The end date of the date range.
        service (IReservationService, optional): The injected reservation service dependency.

    Returns:
        Iterable[Reservation]: A collection of reservations within the given date range.
    """
    reservations = await service.get_between_dates(start_date, end_date)

    return reservations


@router.get("/{reservation_id}", response_model=Reservation, status_code=200)
@inject
async def get_reservation_by_id(
        reservation_id: int,
        service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Reservation | None:
    """
    Get reservation details by ID.

    Args:
        reservation_id (int): The ID of the reservation.
        service (IReservationService, optional): The injected reservation service dependency.

    Returns:
        Reservation | None: The reservation details, or None if not found.

    Raises:
        HTTPException: If the reservation is not found.
    """
    reservation = await service.get_by_id(reservation_id)

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    return reservation


@router.get("/{reservation_id}/cost", response_model=dict, status_code=200)
@inject
async def get_reservation_cost_by_id(
        reservation_id: int,
        service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> dict:
    """
    Get the total cost of a reservation by ID.

    Args:
        reservation_id (int): The ID of the reservation.
        service (IReservationService, optional): The injected reservation service dependency.

    Returns:
        dict: A dictionary containing the total cost of the reservation.

    Raises:
        HTTPException: If the reservation is not found.
    """
    reservation = await service.get_by_id(reservation_id)

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    cost = reservation.get_cost()

    return {"total_cost": cost}


@router.put("/{reservation_id}", response_model=Reservation, status_code=200)
@inject
async def update_reservation(
        reservation_id: int,
        updated_reservation: ReservationIn,
        service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> dict:
    """
    Update an existing reservation.

    Args:
        reservation_id (int): The ID of the reservation.
        updated_reservation (ReservationIn): The updated reservation data.
        service (IReservationService, optional): The injected reservation service dependency.

    Returns:
        dict: The updated reservation details.

    Raises:
        HTTPException: If the reservation does not exist.
    """
    if await service.get_by_id(reservation_id=reservation_id):
        await service.update_reservation(
            reservation_id=reservation_id,
            data=updated_reservation,
        )
        return {**updated_reservation.dict(), "id": reservation_id}

    raise HTTPException(status_code=404, detail="Reservation not found")


@router.delete("/{reservation_id}", status_code=204)
@inject
async def delete_reservation(
        reservation_id: int,
        reservation_service: IReservationService = Depends(Provide[Container.reservation_service]),
        reservation_room_service: IReservationRoomService = Depends(Provide[Container.reservation_room_service]),
        bill_service: IBillService = Depends(Provide[Container.bill_service])
) -> None:
    """
    Delete a reservation by ID.

    Args:
        reservation_id (int): The ID of the reservation.
        reservation_service (IReservationService, optional): The injected reservation service dependency.
        reservation_room_service (IReservationRoomService, optional): The injected reservation_room service dependency.
    Raises:
        HTTPException: If the reservation is not found.
    """

    if not await reservation_service.get_by_id(reservation_id=reservation_id):
        raise HTTPException(status_code=404, detail="Reservation not found")

    await bill_service.delete_bill_by_reservation_id(reservation_id)

    for reservation_room in await reservation_room_service.get_by_reservation_id(reservation_id):
        await reservation_room_service.delete_reservation_room(reservation_room.room_id, reservation_id)

    await reservation_service.delete_reservation(reservation_id)

    return
