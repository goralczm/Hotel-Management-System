"""A module containing continent endpoints."""

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
    """An endpoint for adding new guest_accessibility_option.

    Args:
        guest_accessibility_option (GuestAccessibilityOptionIn): The guest_accessibility_option data.
        guest_service (IGuestService, optional): The injected guest service dependency
        accessibility_option_service (IAccessibilityOptionService, optional): The injected accessibility option service dependency
        guest_accessibility_option_service (IGuestAccessibilityOptionService, optional): The injected service dependency.

    Returns:
        dict: The new guest_accessibility_option attributes.
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
    """An endpoint for getting all guest_accessibility_options.

    Args:
        service (IGuestAccessibilityOptionService, optional): The injected service dependency.

    Returns:
        Iterable: The guest_accessibility_option attributes collection.
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
    """An endpoint for getting guest_accessibility_option by id.

    Args:
        guest_id (int): The id of the guest
        accessibility_option_id (int): The id of the accessibility_option.
        service (IGuestAccessibilityOptionService, optional): The injected service dependency.

    Returns:
        dict | None: The guest_accessibility_option details.
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
    """An endpoint for updating guest_accessibility_option data.

    Args:
        guest_id (int): The id of the guest
        accessibility_option_id (int): The id of the accessibility_option.
        updated_guest_accessibility_option (GuestAccessibilityOptionIn): The updated guest_accessibility_option details.
        service (IGuestAccessibilityOptionService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if guest_accessibility_option does not exist.

    Returns:
        dict: The updated guest_accessibility_option details.
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
    """An endpoint for deleting guest_accessibility_options.

    Args:
        guest_id (int): The id of the guest
        accessibility_option_id (int): The id of the accessibility_option.
        service (IcontinentService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if guest_accessibility_option does not exist.
    """

    if await service.get_by_id(guest_id=guest_id, accessibility_option_id=accessibility_option_id):
        await service.delete_guest_accessibility_option(guest_id, accessibility_option_id)

        return

    raise HTTPException(status_code=404, detail="GuestAccessibilityOption not found")