"""
A module containing room_accessibility_option endpoints.
"""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from hotel_management_system.container import Container
from hotel_management_system.core.services.i_room_service import IRoomService
from hotel_management_system.core.services.i_accessibility_option_service import IAccessibilityOptionService
from hotel_management_system.core.domains.room_accessibility_option import RoomAccessibilityOption, RoomAccessibilityOptionIn
from hotel_management_system.core.services.i_room_accessibility_option_service import IRoomAccessibilityOptionService

router = APIRouter()


@router.post("/create", response_model=RoomAccessibilityOption, status_code=201)
@inject
async def create_room_accessibility_option(
        room_accessibility_option: RoomAccessibilityOptionIn,
        room_service: IRoomService = Depends(Provide[Container.room_service]),
        accessibility_option_service: IAccessibilityOptionService = Depends(Provide[Container.accessibility_option_service]),
        room_accessibility_option_service: IRoomAccessibilityOptionService = Depends(Provide[Container.room_accessibility_option_service]),
) -> dict:
    """
    Create a new room accessibility option by associating a room with an accessibility option.

    Args:
        room_accessibility_option (RoomAccessibilityOptionIn): The room accessibility option data.
        room_service (IRoomService): The room service dependency.
        accessibility_option_service (IAccessibilityOptionService): The accessibility option service dependency.
        room_accessibility_option_service (IRoomAccessibilityOptionService): The room accessibility option service dependency.

    Returns:
        dict: The newly created room accessibility option details.

    Raises:
        HTTPException: If the room or accessibility option doesn't exist.
    """
    if not await room_service.get_by_id(room_accessibility_option.room_id):
        raise HTTPException(status_code=404, detail="Room not found")

    if not await accessibility_option_service.get_by_id(room_accessibility_option.accessibility_option_id):
        raise HTTPException(status_code=404, detail="Accessibility option not found")

    new_room_accessibility_option = await room_accessibility_option_service.add_room_accessibility_option(room_accessibility_option)

    return new_room_accessibility_option.model_dump() if new_room_accessibility_option else {}


@router.get("/all", response_model=Iterable[RoomAccessibilityOption], status_code=200)
@inject
async def get_all_room_accessibility_options(
        service: IRoomAccessibilityOptionService = Depends(Provide[Container.room_accessibility_option_service]),
) -> Iterable:
    """
    Retrieve all room accessibility options.

    Args:
        service (IRoomAccessibilityOptionService): The room accessibility option service dependency.

    Returns:
        Iterable: A collection of room accessibility options.
    """
    room_accessibility_options = await service.get_all()

    return room_accessibility_options


@router.get("/{room_accessibility_option_id}", response_model=RoomAccessibilityOption, status_code=200)
@inject
async def get_room_accessibility_option_by_id(
        room_id: int,
        accessibility_option_id: int,
        service: IRoomAccessibilityOptionService = Depends(Provide[Container.room_accessibility_option_service]),
) -> dict | None:
    """
    Retrieve a room accessibility option by its room and accessibility option IDs.

    Args:
        room_id (int): The ID of the room.
        accessibility_option_id (int): The ID of the accessibility option.
        service (IRoomAccessibilityOptionService): The room accessibility option service dependency.

    Returns:
        dict | None: The room accessibility option details, or None if not found.

    Raises:
        HTTPException: If the room accessibility option doesn't exist.
    """
    room_accessibility_option = await service.get_by_id(room_id, accessibility_option_id)

    if room_accessibility_option:
        return room_accessibility_option.model_dump()

    raise HTTPException(status_code=404, detail="RoomAccessibilityOption not found")


@router.put("/{room_accessibility_option_id}", response_model=RoomAccessibilityOption, status_code=200)
@inject
async def update_room_accessibility_option(
        room_id: int,
        accessibility_option_id: int,
        updated_room_accessibility_option: RoomAccessibilityOptionIn,
        service: IRoomAccessibilityOptionService = Depends(Provide[Container.room_accessibility_option_service]),
) -> dict:
    """
    Update a room accessibility option.

    Args:
        room_id (int): The ID of the room.
        accessibility_option_id (int): The ID of the accessibility option.
        updated_room_accessibility_option (RoomAccessibilityOptionIn): The updated room accessibility option data.
        service (IRoomAccessibilityOptionService): The room accessibility option service dependency.

    Returns:
        dict: The updated room accessibility option details.

    Raises:
        HTTPException: If the room accessibility option doesn't exist.
    """
    if await service.get_by_id(room_id, accessibility_option_id):
        await service.update_room_accessibility_option(
            room_id=room_id,
            accessibility_option_id=accessibility_option_id,
            data=updated_room_accessibility_option,
        )
        return updated_room_accessibility_option.model_dump()

    raise HTTPException(status_code=404, detail="RoomAccessibilityOption not found")


@router.delete("/{room_accessibility_option_id}", status_code=204)
@inject
async def delete_room_accessibility_option(
        room_id: int,
        accessibility_option_id: int,
        service: IRoomAccessibilityOptionService = Depends(Provide[Container.room_accessibility_option_service]),
) -> None:
    """
    Delete a room accessibility option by its room and accessibility option IDs.

    Args:
        room_id (int): The ID of the room.
        accessibility_option_id (int): The ID of the accessibility option.
        service (IRoomAccessibilityOptionService): The room accessibility option service dependency.

    Raises:
        HTTPException: If the room accessibility option doesn't exist.
    """
    if await service.get_by_id(room_id, accessibility_option_id):
        await service.delete_room_accessibility_option(room_id, accessibility_option_id)
        return

    raise HTTPException(status_code=404, detail="RoomAccessibilityOption not found")
