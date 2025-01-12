"""
A module containing room endpoints.
"""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from hotel_management_system.container import Container
from hotel_management_system.core.domains.room import Room, RoomIn
from hotel_management_system.core.services.i_room_service import IRoomService

router = APIRouter()


@router.post("/create", response_model=Room, status_code=201)
@inject
async def create_room(
        room: RoomIn,
        service: IRoomService = Depends(Provide[Container.room_service]),
) -> dict:
    """
    Create a new room in the system.

    Args:
        room (RoomIn): The data for the new room.
        service (IRoomService): The injected room service dependency.

    Returns:
        dict: The newly created room attributes.

    Raises:
        HTTPException: If the room cannot be created.
    """
    new_room = await service.add_room(room)
    return new_room.model_dump() if new_room else {}


@router.get("/all", response_model=Iterable[Room], status_code=200)
@inject
async def get_all_rooms(
        service: IRoomService = Depends(Provide[Container.room_service]),
) -> Iterable:
    """
    Retrieve all rooms in the system.

    Args:
        service (IRoomService): The injected room service dependency.

    Returns:
        Iterable: A collection of rooms.
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
    """
    Retrieve a room by its ID.

    Args:
        room_id (int): The ID of the room.
        service (IRoomService): The injected room service dependency.

    Returns:
        dict | None: The room details or None if not found.

    Raises:
        HTTPException: If the room is not found.
    """
    room = await service.get_by_id(room_id)
    if room:
        return room.model_dump()
    raise HTTPException(status_code=404, detail="Room not found")


@router.put("/{room_id}", response_model=Room, status_code=200)
@inject
async def update_room(
        room_id: int,
        updated_room: RoomIn,
        service: IRoomService = Depends(Provide[Container.room_service]),
) -> dict:
    """
    Update a room's data.

    Args:
        room_id (int): The ID of the room.
        updated_room (RoomIn): The updated room details.
        service (IRoomService): The injected room service dependency.

    Returns:
        dict: The updated room details.

    Raises:
        HTTPException: If the room is not found.
    """
    if await service.get_by_id(room_id):
        await service.update_room(room_id=room_id, data=updated_room)
        return {**updated_room.model_dump(), "id": room_id}
    raise HTTPException(status_code=404, detail="Room not found")


@router.delete("/{room_id}", status_code=204)
@inject
async def delete_room(
        room_id: int,
        service: IRoomService = Depends(Provide[Container.room_service]),
) -> None:
    """
    Delete a room from the system.

    Args:
        room_id (int): The ID of the room to delete.
        service (IRoomService): The injected room service dependency.

    Raises:
        HTTPException: If the room is not found.
    """
    if await service.get_by_id(room_id):
        await service.delete_room(room_id)
        return
    raise HTTPException(status_code=404, detail="Room not found")
