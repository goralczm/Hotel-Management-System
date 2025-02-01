"""A module containing guest accessibility option management endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from hotel_management_system.container import Container
from hotel_management_system.core.services.i_guest_service import IGuestService
from hotel_management_system.core.services.i_accessibility_option_service import IAccessibilityOptionService
from hotel_management_system.core.domains.guest_accessibility_option import GuestAccessibilityOption, GuestAccessibilityOptionIn
from hotel_management_system.core.services.i_guest_accessibility_option_service import IGuestAccessibilityOptionService

router = APIRouter()


@router.post("/create", response_model=GuestAccessibilityOption, status_code=201)
@inject
async def create_guest_accessibility_option(
        guest_accessibility_option: GuestAccessibilityOptionIn,
        guest_service: IGuestService = Depends(Provide[Container.guest_service]),
        accessibility_option_service: IAccessibilityOptionService = Depends(Provide[Container.accessibility_option_service]),
        guest_accessibility_option_service: IGuestAccessibilityOptionService = Depends(Provide[Container.guest_accessibility_option_service]),
) -> dict:
    """
    Create a new guest accessibility option.

    Args:
        guest_accessibility_option (GuestAccessibilityOptionIn): The data for the new guest accessibility option.
        guest_service (IGuestService, optional): The service for validating guest data.
        accessibility_option_service (IAccessibilityOptionService, optional): The service for validating accessibility options.
        guest_accessibility_option_service (IGuestAccessibilityOptionService, optional): The service for managing guest accessibility options.

    Returns:
        dict: The created guest accessibility option's details.

    Raises:
        HTTPException: 404 if the guest or accessibility option does not exist.
    """
    if not await guest_service.get_by_id(guest_accessibility_option.guest_id):
        raise HTTPException(status_code=404, detail="Guest id not found")

    if not await accessibility_option_service.get_by_id(guest_accessibility_option.accessibility_option_id):
        raise HTTPException(status_code=404, detail="Accessibility option id not found")

    new_guest_accessibility_option = await guest_accessibility_option_service.add_guest_accessibility_option(guest_accessibility_option)
    return new_guest_accessibility_option.model_dump() if new_guest_accessibility_option else {}


@router.get("/all", response_model=Iterable[GuestAccessibilityOption], status_code=200)
@inject
async def get_all_guest_accessibility_options(
        service: IGuestAccessibilityOptionService = Depends(Provide[Container.guest_accessibility_option_service]),
) -> Iterable:
    """
    Retrieve all guest accessibility options.

    Args:
        service (IGuestAccessibilityOptionService, optional): The service for fetching all guest accessibility options.

    Returns:
        Iterable: A collection of all guest accessibility options.
    """
    guest_accessibility_options = await service.get_all()
    return guest_accessibility_options


@router.get(
    "/{guest_accessibility_option_id}",
    response_model=GuestAccessibilityOption,
    status_code=200,
)
@inject
async def get_guest_accessibility_option_by_id(
        guest_id: int,
        accessibility_option_id: int,
        service: IGuestAccessibilityOptionService = Depends(Provide[Container.guest_accessibility_option_service]),
) -> dict | None:
    """
    Retrieve a guest accessibility option by guest ID and accessibility option ID.

    Args:
        guest_id (int): The ID of the guest.
        accessibility_option_id (int): The ID of the accessibility option.
        service (IGuestAccessibilityOptionService, optional): The service for fetching guest accessibility options.

    Returns:
        dict | None: The guest accessibility option details if found, else None.

    Raises:
        HTTPException: 404 if the guest accessibility option is not found.
    """
    if guest_accessibility_option := await service.get_by_id(guest_id, accessibility_option_id):
        return guest_accessibility_option.model_dump()

    raise HTTPException(status_code=404, detail="GuestAccessibilityOption not found")


@router.put("/{guest_accessibility_option_id}", response_model=GuestAccessibilityOption, status_code=201)
@inject
async def update_guest_accessibility_option(
        guest_id: int,
        accessibility_option_id: int,
        updated_guest_accessibility_option: GuestAccessibilityOptionIn,
        service: IGuestAccessibilityOptionService = Depends(Provide[Container.guest_accessibility_option_service]),
) -> dict:
    """
    Update a guest accessibility option.

    Args:
        guest_id (int): The ID of the guest.
        accessibility_option_id (int): The ID of the accessibility option.
        updated_guest_accessibility_option (GuestAccessibilityOptionIn): The updated data for the guest accessibility option.
        service (IGuestAccessibilityOptionService, optional): The service for updating guest accessibility options.

    Raises:
        HTTPException: 404 if the guest accessibility option does not exist.

    Returns:
        dict: The updated guest accessibility option details.
    """
    if await service.get_by_id(guest_id=guest_id, accessibility_option_id=accessibility_option_id):
        await service.update_guest_accessibility_option(
            guest_id=guest_id,
            accessibility_option_id=accessibility_option_id,
            data=updated_guest_accessibility_option,
        )
        return {**updated_guest_accessibility_option.model_dump()}

    raise HTTPException(status_code=404, detail="GuestAccessibilityOption not found")


@router.delete("/{guest_accessibility_option_id}", status_code=204)
@inject
async def delete_guest_accessibility_option(
        guest_id: int,
        accessibility_option_id: int,
        service: IGuestAccessibilityOptionService = Depends(Provide[Container.guest_accessibility_option_service]),
) -> None:
    """
    Delete a guest accessibility option.

    Args:
        guest_id (int): The ID of the guest.
        accessibility_option_id (int): The ID of the accessibility option.
        service (IGuestAccessibilityOptionService, optional): The service for deleting guest accessibility options.

    Raises:
        HTTPException: 404 if the guest accessibility option does not exist.
    """
    if await service.get_by_id(guest_id=guest_id, accessibility_option_id=accessibility_option_id):
        await service.delete_guest_accessibility_option(guest_id, accessibility_option_id)
        return

    raise HTTPException(status_code=404, detail="GuestAccessibilityOption not found")
