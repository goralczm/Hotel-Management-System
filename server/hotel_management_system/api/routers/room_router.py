"""
A module containing room endpoints.
"""

from typing import Iterable, List
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from hotel_management_system.container import Container
from hotel_management_system.core.domains.room import Room, RoomIn
from hotel_management_system.core.domains.room_accessibility_option import RoomAccessibilityOptionIn
from hotel_management_system.core.services.i_accessibility_option_service import IAccessibilityOptionService
from hotel_management_system.core.services.i_room_accessibility_option_service import IRoomAccessibilityOptionService
from hotel_management_system.core.services.i_room_service import IRoomService

router = APIRouter()


@router.post("/create", response_model=Room, status_code=201)
@inject
async def create_room(
        room: RoomIn,
        accessibility_option_ids: List[int] = [-1],
        accessibility_option_service: IAccessibilityOptionService =
        Depends(Provide[Container.accessibility_option_service]),
        room_accessibility_option_service: IRoomAccessibilityOptionService =
        Depends(Provide[Container.room_accessibility_option_service]),
        room_service: IRoomService = Depends(Provide[Container.room_service]),
) -> dict:
    """
    Create a new room in the system.

    Args:
        room (RoomIn): The data for the new room.
        accessibility_option_ids (List[int]): The list of accessibility option ids for the new room.
        accessibility_option_service (IAccessibilityOptionService): The injected accessibility option service dependency
        room_accessibility_option_service (IRoomAccessibilityOptionService): The injected room accessibility option
                                                                                                    service dependency.
        room_service (IRoomService): The injected room service dependency.

    Returns:
        dict: The newly created room attributes.

    Raises:
        HTTPException 404: If the accessibility option is not found.
    """
    new_room = await room_service.add_room(room)

    if new_room:
        for accessibility_option_id in accessibility_option_ids:
            if await accessibility_option_service.get_by_id(accessibility_option_id):
                await room_accessibility_option_service.add_room_accessibility_option(
                    RoomAccessibilityOptionIn(
                        room_id=new_room.id,
                        accessibility_option_id=accessibility_option_id,
                    )
                )
            else:
                await room_service.delete_room(new_room.id)
                raise HTTPException(status_code=404, detail="Accessibility option not found")

    return new_room if new_room else {}


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
        room_accessibility_option_service: IRoomAccessibilityOptionService =
        Depends(Provide[Container.room_accessibility_option_service]),
        room_service: IRoomService = Depends(Provide[Container.room_service]),
) -> None:
    """
    Delete a room from the system.

    Args:
        room_id (int): The ID of the room to delete.
        room_accessibility_option_service (IRoomAccessibilityOptionService): The injected room accessibility option
                                                                                                    service dependency.
        room_service (IRoomService): The injected room service dependency.

    Raises:
        HTTPException: 404 If the room is not found.
    """
    room = await room_service.get_by_id(room_id)

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    await room_service.delete_room(room_id)

    for accessibility_option in room.accessibility_options:
        await room_accessibility_option_service.delete_room_accessibility_option(room.id, accessibility_option.id)

    return
