"""A module containing continent endpoints."""

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
    """An endpoint for adding new room_accessibility_option.

    Args:
        room_accessibility_option (RoomAccessibilityOptionIn): The room_accessibility_option data.
        room_service (IRoomService, optional): The injected room service dependency
        accessibility_option_service (IAccessibilityOptionService, optional): The injected accessibility option service dependency
        room_accessibility_option_service (IRoomAccessibilityOptionService, optional): The injected service dependency.

    Returns:
        dict: The new room_accessibility_option attributes.
    """

    if not await room_service.get_by_id(room_accessibility_option.room_id):
        raise HTTPException(status_code=404, detail="Room id not found")

    if not await accessibility_option_service.get_by_id(room_accessibility_option.accessibility_option_id):
        raise HTTPException(status_code=404, detail="Accessibility option id not found")

    new_room_accessibility_option = await room_accessibility_option_service.add_room_accessibility_option(room_accessibility_option)

    return new_room_accessibility_option.model_dump() if new_room_accessibility_option else {}


@router.get("/all", response_model=Iterable[RoomAccessibilityOption], status_code=200)
@inject
async def get_all_room_accessibility_options(
        service: IRoomAccessibilityOptionService = Depends(Provide[Container.room_accessibility_option_service]),
) -> Iterable:
    """An endpoint for getting all room_accessibility_options.

    Args:
        service (IRoomAccessibilityOptionService, optional): The injected service dependency.

    Returns:
        Iterable: The room_accessibility_option attributes collection.
    """

    room_accessibility_options = await service.get_all()

    return room_accessibility_options


@router.get(
    "/{room_accessibility_option_id}",
    response_model=RoomAccessibilityOption,
    status_code=200,
)
@inject
async def get_room_accessibility_option_by_id(
        room_id: int,
        accessibility_option_id: int,
        service: IRoomAccessibilityOptionService = Depends(Provide[Container.room_accessibility_option_service]),
) -> dict | None:
    """An endpoint for getting room_accessibility_option by id.

    Args:
        room_id (int): The id of the room
        accessibility_option_id (int): The id of the accessibility_option.
        service (IRoomAccessibilityOptionService, optional): The injected service dependency.

    Returns:
        dict | None: The room_accessibility_option details.
    """

    if room_accessibility_option := await service.get_by_id(room_id, accessibility_option_id):
        return room_accessibility_option.model_dump()

    raise HTTPException(status_code=404, detail="RoomAccessibilityOption not found")


@router.put("/{room_accessibility_option_id}", response_model=RoomAccessibilityOption, status_code=201)
@inject
async def update_room_accessibility_option(
        room_id: int,
        accessibility_option_id: int,
        updated_room_accessibility_option: RoomAccessibilityOptionIn,
        service: IRoomAccessibilityOptionService = Depends(Provide[Container.room_accessibility_option_service]),
) -> dict:
    """An endpoint for updating room_accessibility_option data.

    Args:
        room_id (int): The id of the room
        accessibility_option_id (int): The id of the accessibility_option.
        updated_room_accessibility_option (RoomAccessibilityOptionIn): The updated room_accessibility_option details.
        service (IRoomAccessibilityOptionService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if room_accessibility_option does not exist.

    Returns:
        dict: The updated room_accessibility_option details.
    """

    if await service.get_by_id(room_id=room_id, accessibility_option_id=accessibility_option_id):
        await service.update_room_accessibility_option(
            room_id=room_id,
            accessibility_option_id=accessibility_option_id,
            data=updated_room_accessibility_option,
        )
        return {**updated_room_accessibility_option.model_dump()}

    raise HTTPException(status_code=404, detail="RoomAccessibilityOption not found")


@router.delete("/{room_accessibility_option_id}", status_code=204)
@inject
async def delete_room_accessibility_option(
        room_id: int,
        accessibility_option_id: int,
        service: IRoomAccessibilityOptionService = Depends(Provide[Container.room_accessibility_option_service]),
) -> None:
    """An endpoint for deleting room_accessibility_options.

    Args:
        room_id (int): The id of the room
        accessibility_option_id (int): The id of the accessibility_option.
        service (IcontinentService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if room_accessibility_option does not exist.
    """

    if await service.get_by_id(room_id=room_id, accessibility_option_id=accessibility_option_id):
        await service.delete_room_accessibility_option(room_id, accessibility_option_id)

        return

    raise HTTPException(status_code=404, detail="RoomAccessibilityOption not found")