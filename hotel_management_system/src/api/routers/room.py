"""A module containing continent endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from hotel_management_system.src.container import Container
from hotel_management_system.src.core.domains.room import Room, RoomIn
from hotel_management_system.src.core.services.i_room_service import IRoomService

router = APIRouter()


@router.post("/create", response_model=Room, status_code=201)
@inject
async def create_room(
        room: RoomIn,
        service: IRoomService = Depends(Provide[Container.room_service]),
) -> dict:
    """An endpoint for adding new room.

    Args:
        room (RoomIn): The room data.
        service (IRoomService, optional): The injected service dependency.

    Returns:
        dict: The new room attributes.
    """

    new_room = await service.add_room(room)

    return new_room.model_dump() if new_room else {}


@router.get("/all", response_model=Iterable[Room], status_code=200)
@inject
async def get_all_rooms(
        service: IRoomService = Depends(Provide[Container.room_service]),
) -> Iterable:
    """An endpoint for getting all rooms.

    Args:
        service (IRoomService, optional): The injected service dependency.

    Returns:
        Iterable: The room attributes collection.
    """

    rooms = await service.get_all()

    return rooms


@router.get(
    "/{room_id}",
    response_model=Room,
    status_code=200,
)
@inject
async def get_room_by_id(
        room_id: int,
        service: IRoomService = Depends(Provide[Container.room_service]),
) -> dict | None:
    """An endpoint for getting room by id.

    Args:
        room_id (int): The id of the room.
        service (IRoomService, optional): The injected service dependency.

    Returns:
        dict | None: The room details.
    """

    if room := await service.get_by_id(room_id):
        return room.model_dump()

    raise HTTPException(status_code=404, detail="Room not found")


@router.put("/{room_id}", response_model=Room, status_code=201)
@inject
async def update_room(
        room_id: int,
        updated_room: RoomIn,
        service: IRoomService = Depends(Provide[Container.room_service]),
) -> dict:
    """An endpoint for updating room data.

    Args:
        room_id (int): The id of the room.
        updated_room (RoomIn): The updated room details.
        service (IRoomtService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if room does not exist.

    Returns:
        dict: The updated room details.
    """

    if await service.get_by_id(room_id=room_id):
        await service.update_room(
            room_id=room_id,
            data=updated_room,
        )
        return {**updated_room.model_dump(), "id": room_id}

    raise HTTPException(status_code=404, detail="Room not found")


@router.delete("/{room_id}", status_code=204)
@inject
async def delete_room(
        room_id: int,
        service: IRoomService = Depends(Provide[Container.room_service]),
) -> None:
    """An endpoint for deleting rooms.

    Args:
        room_id (int): The id of the room.
        service (IcontinentService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if room does not exist.
    """

    if await service.get_by_id(room_id=room_id):
        await service.delete_room(room_id)

        return

    raise HTTPException(status_code=404, detail="Room not found")