"""A module containing continent endpoints."""

from typing import Iterable
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
    """An endpoint for adding new accessibility_option.

    Args:
        accessibility_option (AccessibilityOptionIn): The accessibility_option data.
        service (IAccessibilityOptionService, optional): The injected service dependency.

    Returns:
        dict: The new accessibility_option attributes.
    """

    new_accessibility_option = await service.add_accessibility_option(accessibility_option)

    return new_accessibility_option.model_dump() if new_accessibility_option else {}


@router.get("/all", response_model=Iterable[AccessibilityOption], status_code=200)
@inject
async def get_all_accessibility_options(
        service: IAccessibilityOptionService = Depends(Provide[Container.accessibility_option_service]),
) -> Iterable:
    """An endpoint for getting all accessibility_options.

    Args:
        service (IAccessibilityOptionService, optional): The injected service dependency.

    Returns:
        Iterable: The accessibility_option attributes collection.
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
    """An endpoint for getting accessibility_option by id.

    Args:
        accessibility_option_id (int): The id of the accessibility_option.
        service (IAccessibilityOptionService, optional): The injected service dependency.

    Returns:
        dict | None: The accessibility_option details.
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
    """An endpoint for updating accessibility_option data.

    Args:
        accessibility_option_id (int): The id of the accessibility_option.
        updated_accessibility_option (AccessibilityOptionIn): The updated accessibility_option details.
        service (IAccessibilityOptiontService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if accessibility_option does not exist.

    Returns:
        dict: The updated accessibility_option details.
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
    """An endpoint for deleting accessibility_options.

    Args:
        accessibility_option_id (int): The id of the accessibility_option.
        service (IcontinentService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if accessibility_option does not exist.
    """

    if await service.get_by_id(accessibility_option_id=accessibility_option_id):
        await service.delete_accessibility_option(accessibility_option_id)

        return

    raise HTTPException(status_code=404, detail="AccessibilityOption not found")