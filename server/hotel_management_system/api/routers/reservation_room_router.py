"""A module containing reservation_room endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from hotel_management_system.container import Container
from hotel_management_system.core.services.i_reservation_service import IReservationService
from hotel_management_system.core.services.i_room_service import IRoomService
from hotel_management_system.core.domains.reservation_room import ReservationRoom, ReservationRoomIn
from hotel_management_system.core.services.i_reservation_room_service import IReservationRoomService

router = APIRouter()


@router.post("/create", response_model=ReservationRoom, status_code=201)
@inject
async def create_reservation_room(
        reservation_room: ReservationRoomIn,
        room_service: IRoomService = Depends(Provide[Container.room_service]),
        reservation_service: IReservationService = Depends(Provide[Container.reservation_service]),
        reservation_room_service: IReservationRoomService = Depends(Provide[Container.reservation_room_service]),
) -> dict:
    """
    Create a new reservation room.

    Args:
        reservation_room (ReservationRoomIn): The reservation room data to be added.
        room_service (IRoomService, optional): The injected room service dependency.
        reservation_service (IReservationService, optional): The injected reservation service dependency.
        reservation_room_service (IReservationRoomService, optional): The injected reservation room service dependency.

    Returns:
        dict: The attributes of the newly created reservation room.

    Raises:
        HTTPException: If the room ID or reservation ID is not found.
    """
    if not await room_service.get_by_id(reservation_room.room_id):
        raise HTTPException(status_code=404, detail="Room id not found")

    if not await reservation_service.get_by_id(reservation_room.reservation_id):
        raise HTTPException(status_code=404, detail="Reservation id not found")

    new_reservation_room = await reservation_room_service.add_reservation_room(reservation_room)

    return new_reservation_room.model_dump() if new_reservation_room else {}


@router.get("/all", response_model=Iterable[ReservationRoom], status_code=200)
@inject
async def get_all_reservation_rooms(
        service: IReservationRoomService = Depends(Provide[Container.reservation_room_service]),
) -> Iterable:
    """
    Retrieve all reservation rooms.

    Args:
        service (IReservationRoomService, optional): The injected reservation room service dependency.

    Returns:
        Iterable: A collection of reservation room attributes.
    """
    reservation_rooms = await service.get_all()

    return reservation_rooms


@router.get("/room_id/{room_id}", response_model=ReservationRoom, status_code=200)
@inject
async def get_reservation_room_by_id(
        room_id: int,
        reservation_id: int,
        service: IReservationRoomService = Depends(Provide[Container.reservation_room_service]),
) -> dict | None:
    """
    Retrieve a specific reservation room by room ID and reservation ID.

    Args:
        room_id (int): The ID of the room.
        reservation_id (int): The ID of the reservation.
        service (IReservationRoomService, optional): The injected reservation room service dependency.

    Returns:
        dict | None: The reservation room details, or None if not found.

    Raises:
        HTTPException: If the reservation room is not found.
    """
    if reservation_room := await service.get_by_id(room_id, reservation_id):
        return reservation_room.model_dump()

    raise HTTPException(status_code=404, detail="ReservationRoom not found")


@router.put("/{room_reservation_id}", response_model=ReservationRoom, status_code=201)
@inject
async def update_reservation_room(
        room_id: int,
        reservation_id: int,
        updated_reservation_room: ReservationRoomIn,
        service: IReservationRoomService = Depends(Provide[Container.reservation_room_service]),
) -> dict:
    """
    Update the details of an existing reservation room.

    Args:
        room_id (int): The ID of the room.
        reservation_id (int): The ID of the reservation.
        updated_reservation_room (ReservationRoomIn): The updated reservation room data.
        service (IReservationRoomService, optional): The injected reservation room service dependency.

    Returns:
        dict: The updated reservation room details.

    Raises:
        HTTPException: If the reservation room does not exist.
    """
    if await service.get_by_id(room_id=room_id, reservation_id=reservation_id):
        await service.update_reservation_room(
            room_id=room_id,
            reservation_id=reservation_id,
            data=updated_reservation_room,
        )
        return {**updated_reservation_room.model_dump()}

    raise HTTPException(status_code=404, detail="ReservationRoom not found")


@router.delete("/{room_reservation_id}", status_code=204)
@inject
async def delete_reservation_room(
        room_id: int,
        reservation_id: int,
        service: IReservationRoomService = Depends(Provide[Container.reservation_room_service]),
) -> None:
    """
    Delete an existing reservation room.

    Args:
        room_id (int): The ID of the room.
        reservation_id (int): The ID of the reservation.
        service (IReservationRoomService, optional): The injected reservation room service dependency.

    Raises:
        HTTPException: If the reservation room does not exist.
    """
    if await service.get_by_id(room_id=room_id, reservation_id=reservation_id):
        await service.delete_reservation_room(room_id, reservation_id)
        return

    raise HTTPException(status_code=404, detail="ReservationRoom not found")
