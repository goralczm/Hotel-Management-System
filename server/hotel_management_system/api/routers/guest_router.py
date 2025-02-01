"""A module containing guest management endpoints."""

from typing import List
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from hotel_management_system.container import Container
from hotel_management_system.core.domains.guest import Guest, GuestIn
from hotel_management_system.core.domains.guest_accessibility_option import GuestAccessibilityOptionIn
from hotel_management_system.core.services.i_accessibility_option_service import IAccessibilityOptionService
from hotel_management_system.core.services.i_guest_accessibility_option_service import IGuestAccessibilityOptionService
from hotel_management_system.core.services.i_guest_service import IGuestService

router = APIRouter()


@router.post("/create", response_model=Guest, status_code=201)
@inject
async def create_guest(
        guest: GuestIn,
        accessibility_option_ids: List[int] = [-1],
        guest_service: IGuestService = Depends(Provide[Container.guest_service]),
        accessibility_option_service: IAccessibilityOptionService =
        Depends(Provide[Container.accessibility_option_service]),
        guest_accessibility_option_service: IGuestAccessibilityOptionService =
        Depends(Provide[Container.guest_accessibility_option_service]),
) -> dict:
    """
    Create a new guest.

    Args:
        guest (GuestIn): The guest data to be added.
        accessibility_option_ids (List[int], optional): The list of accessibility option ids for the new guest.
        guest_service (IGuestService, optional): The service for managing guest data.
        accessibility_option_service (IAccessibilityOptionService, optional): The service for managing accessibility
                                                                                                    option data.
        guest_accessibility_option_service (IGuestAccessibilityOptionService, optional): The service for managing guest
                                                                                                    accessibility data.

    Returns:
        dict: The details of the newly created guest.

    Raises:
        HTTPException: 404 if the accessibility option not found.
    """
    new_guest = await guest_service.add_guest(guest)

    if new_guest:
        for accessibility_option_id in accessibility_option_ids:
            if accessibility_option_id == -1:
                continue

            if await accessibility_option_service.get_by_id(accessibility_option_id):
                await guest_accessibility_option_service.add_guest_accessibility_option(
                    GuestAccessibilityOptionIn(
                        guest_id=new_guest.id,
                        accessibility_option_id=accessibility_option_id,
                    )
                )
            else:
                await guest_service.delete_guest(new_guest.id)
                raise HTTPException(status_code=404, detail="Accessibility option not found")

        new_guest = await guest_service.get_by_id(new_guest.id)

    return new_guest if new_guest else {}


@router.get("/all", response_model=List[Guest], status_code=200)
@inject
async def get_all_guests(
        guest_service: IGuestService = Depends(Provide[Container.guest_service]),
) -> List:
    """
    Retrieve all guests.

    Args:
        guest_service (IGuestService, optional): The service for fetching all guest data.

    Returns:
        List: A collection of all guests.
    """
    guests = await guest_service.get_all()

    return guests


@router.get("/{guest_id}", response_model=Guest, status_code=200)
@inject
async def get_guest_by_id(
        guest_id: int,
        guest_service: IGuestService = Depends(Provide[Container.guest_service]),
) -> dict | None:
    """
    Retrieve a guest by their ID.

    Args:
        guest_id (int): The ID of the guest to retrieve.
        guest_service (IGuestService, optional): The service for fetching guest data.

    Returns:
        dict | None: The guest details if found, or None if not found.

    Raises:
        HTTPException: 404 if the guest does not exist.
    """
    if guest := await guest_service.get_by_id(guest_id):
        return guest

    raise HTTPException(status_code=404, detail="Guest not found")


@router.get("/first_name/{first_name}", response_model=List[Guest], status_code=200)
@inject
async def get_guest_by_first_name(
        first_name: str,
        guest_service: IGuestService = Depends(Provide[Container.guest_service]),
) -> dict | None:
    """
    Retrieve guests by their first name.

    Args:
        first_name (str): The first name to search for.
        guest_service (IGuestService, optional): The service for fetching guest data.

    Returns:
        List[Guest]: A list of guests with the matching first name.
    """
    if guests := await guest_service.get_by_first_name(first_name):
        return guests


@router.get("/last_name/{last_name}", response_model=List[Guest], status_code=200)
@inject
async def get_guest_by_last_name(
        last_name: str,
        guest_service: IGuestService = Depends(Provide[Container.guest_service]),
) -> dict | None:
    """
    Retrieve guests by their last name.

    Args:
        last_name (str): The last name to search for.
        guest_service (IGuestService, optional): The service for fetching guest data.

    Returns:
        List[Guest]: A list of guests with the matching last name.
    """
    if guests := await guest_service.get_by_last_name(last_name):
        return guests


@router.get("/needle/{needle}", response_model=List[Guest], status_code=200)
@inject
async def get_by_needle_in_name(
        needle: str,
        guest_service: IGuestService = Depends(Provide[Container.guest_service]),
) -> dict | None:
    """
    Retrieve guests by a needle (substring) in their first or last name.

    Args:
        needle (str): The substring to search for in names.
        guest_service (IGuestService, optional): The service for fetching guest data.

    Returns:
        List[Guest]: A list of guests whose first or last name contains the given needle.
    """
    if guests := await guest_service.get_by_needle_in_name(needle):
        return guests


@router.put("/{guest_id}", response_model=Guest, status_code=201)
@inject
async def update_guest(
        guest_id: int,
        updated_guest: GuestIn,
        guest_service: IGuestService = Depends(Provide[Container.guest_service]),
) -> dict:
    """
    Update guest data.

    Args:
        guest_id (int): The ID of the guest to update.
        updated_guest (GuestIn): The updated guest details.
        guest_service (IGuestService, optional): The service for updating guest data.

    Raises:
        HTTPException: 404 if the guest does not exist.

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
    """
    Delete a guest along with their accessibility options.

    Args:
        guest_id (int): The ID of the guest to delete.
        guest_service (IGuestService, optional): The service for managing guest data.
        guest_accessibility_option_service (IGuestAccessibilityOptionService, optional): The service for managing guest accessibility options.

    Raises:
        HTTPException: 404 if the guest does not exist.
    """
    if not await guest_service.get_by_id(guest_id=guest_id):
        raise HTTPException(status_code=404, detail="Guest not found")

    guest_accessibility_options = await guest_accessibility_option_service.get_by_guest_id(guest_id)
    for guest_accessibility_option in guest_accessibility_options:
        await guest_accessibility_option_service.delete_guest_accessibility_option(guest_id,
                                                                                   guest_accessibility_option.accessibility_option_id)

    await guest_service.delete_guest(guest_id)

    return
