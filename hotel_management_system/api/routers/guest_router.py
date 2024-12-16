"""A module containing continent endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from hotel_management_system.container import Container
from hotel_management_system.core.domains.guest import Guest, GuestIn
from hotel_management_system.core.services.i_guest_accessibility_option_service import IGuestAccessibilityOptionService
from hotel_management_system.core.services.i_guest_service import IGuestService

router = APIRouter()


@router.post("/create", response_model=Guest, status_code=201)
@inject
async def create_guest(
        guest: GuestIn,
        guest_service: IGuestService = Depends(Provide[Container.guest_service])
) -> dict:
    """An endpoint for adding new guest.

    Args:
        guest (GuestIn): The guest data.
        guest_service (IGuestService, optional): The injected service dependency.

    Returns:
        dict: The new guest attributes.
    """

    new_guest = await guest_service.add_guest(guest)

    return new_guest.model_dump() if new_guest else {}


@router.get("/all", response_model=Iterable[Guest], status_code=200)
@inject
async def get_all_guests(
        guest_service: IGuestService = Depends(Provide[Container.guest_service]),
) -> Iterable:
    """An endpoint for getting all guests.

    Args:
        guest_service (IGuestService, optional): The injected service dependency.

    Returns:
        Iterable: The guest attributes collection.
    """

    guests = await guest_service.get_all()

    return guests


@router.get(
    "/{guest_id}",
    response_model=Guest,
    status_code=200,
)
@inject
async def get_guest_by_id(
        guest_id: int,
        guest_service: IGuestService = Depends(Provide[Container.guest_service]),
) -> dict | None:
    """An endpoint for getting guest by id.

    Args:
        guest_id (int): The id of the guest.
        guest_service (IGuestService, optional): The injected service dependency.

    Returns:
        dict | None: The guest details.
    """

    if guest := await guest_service.get_by_id(guest_id):
        return guest.model_dump()

    raise HTTPException(status_code=404, detail="Guest not found")


@router.put("/{guest_id}", response_model=Guest, status_code=201)
@inject
async def update_guest(
        guest_id: int,
        updated_guest: GuestIn,
        guest_service: IGuestService = Depends(Provide[Container.guest_service]),
) -> dict:
    """An endpoint for updating guest data.

    Args:
        guest_id (int): The id of the guest.
        updated_guest (GuestIn): The updated guest details.
        guest_service (IGuestService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if guest does not exist.

    Returns:
        dict: The updated guest details.
    """

    if await guest_service.get_by_id(guest_id=guest_id):
        await guest_service.update_guest(
            guest_id=guest_id,
            data=updated_guest,
        )
        return {**updated_guest.model_dump(), "id": guest_id}

    raise HTTPException(status_code=404, detail="Guest not found")


@router.delete("/{guest_id}", status_code=204)
@inject
async def delete_guest(
        guest_id: int,
        guest_service: IGuestService = Depends(Provide[Container.guest_service]),
        guest_accessibility_option_service: IGuestAccessibilityOptionService = Depends(
            Provide[Container.guest_accessibility_option_service]),
) -> None:
    """An endpoint for deleting guests.

    Args:
        guest_id (int): The id of the guest.
        guest_service (IGuestService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if guest does not exist.
    """

    if not await guest_service.get_by_id(guest_id=guest_id):
        raise HTTPException(status_code=404, detail="Guest not found")

    guest_accessibility_options = await guest_accessibility_option_service.get_by_guest_id(guest_id)
    for guest_accessibility_option in guest_accessibility_options:
        await guest_accessibility_option_service.delete_guest_accessibility_option(guest_id,
                                                                                   guest_accessibility_option.accessibility_option_id)

    await guest_service.delete_guest(guest_id)

    return
