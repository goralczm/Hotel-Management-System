"""
Module containing endpoints for managing accessibility options.
"""

from typing import List
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from hotel_management_system.container import Container
from hotel_management_system.core.domains.accessibility_option import AccessibilityOption, AccessibilityOptionIn
from hotel_management_system.core.services.i_accessibility_option_service import IAccessibilityOptionService

router = APIRouter()


@router.post("/create", response_model=AccessibilityOption, status_code=201)
@inject
async def create_accessibility_option(
        accessibility_option: AccessibilityOptionIn,
        service: IAccessibilityOptionService = Depends(Provide[Container.accessibility_option_service]),
) -> dict:
    """
    Create a new accessibility option.

    Args:
        accessibility_option (AccessibilityOptionIn): The details of the accessibility option to be added.
        service (IAccessibilityOptionService, optional): The service used to add the accessibility option.

    Returns:
        dict: The newly created accessibility option's attributes.
    """
    new_accessibility_option = await service.add_accessibility_option(accessibility_option)
    return new_accessibility_option.model_dump() if new_accessibility_option else {}


@router.get("/all", response_model=List[AccessibilityOption], status_code=200)
@inject
async def get_all_accessibility_options(
        service: IAccessibilityOptionService = Depends(Provide[Container.accessibility_option_service]),
) -> List:
    """
    Retrieve all accessibility options.

    Args:
        service (IAccessibilityOptionService, optional): The service used to fetch all accessibility options.

    Returns:
        List: A list of all accessibility options.
    """
    accessibility_options = await service.get_all()
    return accessibility_options


@router.get(
    "/{accessibility_option_id}",
    response_model=AccessibilityOption,
    status_code=200,
)
@inject
async def get_accessibility_option_by_id(
        accessibility_option_id: int,
        service: IAccessibilityOptionService = Depends(Provide[Container.accessibility_option_service]),
) -> dict | None:
    """
    Retrieve an accessibility option by its ID.

    Args:
        accessibility_option_id (int): The ID of the accessibility option.
        service (IAccessibilityOptionService, optional): The service used to fetch the accessibility option by ID.

    Returns:
        dict | None: The details of the accessibility option if found, else None.
    Raises:
        HTTPException: 404 if the accessibility option with the given ID does not exist.
    """
    if accessibility_option := await service.get_by_id(accessibility_option_id):
        return accessibility_option.model_dump()

    raise HTTPException(status_code=404, detail="AccessibilityOption not found")


@router.put("/{accessibility_option_id}", response_model=AccessibilityOption, status_code=201)
@inject
async def update_accessibility_option(
        accessibility_option_id: int,
        updated_accessibility_option: AccessibilityOptionIn,
        service: IAccessibilityOptionService = Depends(Provide[Container.accessibility_option_service]),
) -> dict:
    """
    Update an existing accessibility option.

    Args:
        accessibility_option_id (int): The ID of the accessibility option to be updated.
        updated_accessibility_option (AccessibilityOptionIn): The updated details for the accessibility option.
        service (IAccessibilityOptionService, optional): The service used to update the accessibility option.

    Raises:
        HTTPException: 404 if the accessibility option with the given ID does not exist.

    Returns:
        dict: The updated accessibility option's details.
    """
    if await service.get_by_id(accessibility_option_id=accessibility_option_id):
        await service.update_accessibility_option(
            accessibility_option_id=accessibility_option_id,
            data=updated_accessibility_option,
        )
        return {**updated_accessibility_option.model_dump(), "id": accessibility_option_id}

    raise HTTPException(status_code=404, detail="AccessibilityOption not found")


@router.delete("/{accessibility_option_id}", status_code=204)
@inject
async def delete_accessibility_option(
        accessibility_option_id: int,
        service: IAccessibilityOptionService = Depends(Provide[Container.accessibility_option_service]),
) -> None:
    """
    Delete an accessibility option.

    Args:
        accessibility_option_id (int): The ID of the accessibility option to be deleted.
        service (IAccessibilityOptionService, optional): The service used to delete the accessibility option.

    Raises:
        HTTPException: 404 if the accessibility option with the given ID does not exist.
    """
    if await service.get_by_id(accessibility_option_id=accessibility_option_id):
        await service.delete_accessibility_option(accessibility_option_id)
        return

    raise HTTPException(status_code=404, detail="AccessibilityOption not found")
