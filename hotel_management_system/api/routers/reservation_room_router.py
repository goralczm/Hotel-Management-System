"""A module containing continent endpoints."""

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
    """An endpoint for adding new reservation_room.

    Args:
        reservation_room (ReservationRoomIn): The reservation_room data.
        room_service (IRoomService, optional): The injected room service dependency
        reservation_service (IReservationService, optional): The injected reservation service dependency
        reservation_room_service (IReservationRoomService, optional): The injected service dependency.

    Returns:
        dict: The new reservation_room attributes.
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
    """An endpoint for getting all reservation_rooms.

    Args:
        service (IReservationRoomService, optional): The injected service dependency.

    Returns:
        Iterable: The reservation_room attributes collection.
    """

    reservation_rooms = await service.get_all()

    return reservation_rooms

@router.get(
    "/room_id/{room_id}",
    response_model=ReservationRoom,
    status_code=200,
)
@inject
async def get_reservation_room_by_id(
        room_id: int,
        reservation_id: int,
        service: IReservationRoomService = Depends(Provide[Container.reservation_room_service]),
) -> dict | None:
    """An endpoint for getting reservation_room by id.

    Args:
        room_id (int): The id of the room
        reservation_id (int): The id of the accessibility_option.
        service (IReservationRoomService, optional): The injected service dependency.

    Returns:
        dict | None: The reservation_room details.
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
    """An endpoint for updating reservation_room data.

    Args:
        room_id (int): The id of the room
        reservation_id (int): The id of the accessibility_option.
        updated_reservation_room (ReservationRoomIn): The updated reservation_room details.
        service (IReservationRoomService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if reservation_room does not exist.

    Returns:
        dict: The updated reservation_room details.
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
    """An endpoint for deleting reservation_rooms.

    Args:
        room_id (int): The id of the room
        reservation_id (int): The id of the accessibility_option.
        service (IcontinentService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if reservation_room does not exist.
    """

    if await service.get_by_id(room_id=room_id, reservation_id=reservation_id):
        await service.delete_reservation_room(room_id, reservation_id)

        return

    raise HTTPException(status_code=404, detail="ReservationRoom not found")