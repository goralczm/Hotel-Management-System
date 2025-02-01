"""A module containing pricing detail management endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from hotel_management_system.container import Container
from hotel_management_system.core.domains.pricing_detail import PricingDetail, PricingDetailIn
from hotel_management_system.core.services.i_pricing_detail_service import IPricingDetailService

router = APIRouter()


@router.post("/create", response_model=PricingDetail, status_code=201)
@inject
async def create_pricing_detail(
        pricing_detail: PricingDetailIn,
        pricing_detail_service: IPricingDetailService = Depends(Provide[Container.pricing_detail_service])
) -> dict:
    """
    Create a new pricing detail.

    Args:
        pricing_detail (PricingDetailIn): The pricing detail data to be added.
        pricing_detail_service (IPricingDetailService, optional): The service for managing pricing details.

    Returns:
        dict: The details of the newly created pricing detail.

    Raises:
        HTTPException: 400 if the pricing detail creation fails.
    """
    new_pricing_detail = await pricing_detail_service.add_pricing_detail(pricing_detail)
    return new_pricing_detail.model_dump() if new_pricing_detail else {}


@router.get("/all", response_model=Iterable[PricingDetail], status_code=200)
@inject
async def get_all_pricing_details(
        pricing_detail_service: IPricingDetailService = Depends(Provide[Container.pricing_detail_service]),
) -> Iterable:
    """
    Retrieve all pricing details.

    Args:
        pricing_detail_service (IPricingDetailService, optional): The service for fetching all pricing details.

    Returns:
        Iterable: A collection of all pricing details.
    """
    pricing_details = await pricing_detail_service.get_all()
    return pricing_details


@router.get(
    "/{pricing_detail_id}",
    response_model=PricingDetail,
    status_code=200,
)
@inject
async def get_pricing_detail_by_id(
        pricing_detail_id: int,
        pricing_detail_service: IPricingDetailService = Depends(Provide[Container.pricing_detail_service]),
) -> dict | None:
    """
    Retrieve a pricing detail by its ID.

    Args:
        pricing_detail_id (int): The ID of the pricing detail to retrieve.
        pricing_detail_service (IPricingDetailService, optional): The service for fetching pricing detail data.

    Returns:
        dict | None: The pricing detail details if found, or None if not found.

    Raises:
        HTTPException: 404 if the pricing detail does not exist.
    """
    if pricing_detail := await pricing_detail_service.get_by_id(pricing_detail_id):
        return pricing_detail.model_dump()

    raise HTTPException(status_code=404, detail="PricingDetail not found")


@router.put("/{pricing_detail_id}", response_model=PricingDetail, status_code=201)
@inject
async def update_pricing_detail(
        pricing_detail_id: int,
        updated_pricing_detail: PricingDetailIn,
        pricing_detail_service: IPricingDetailService = Depends(Provide[Container.pricing_detail_service]),
) -> dict:
    """
    Update pricing detail data.

    Args:
        pricing_detail_id (int): The ID of the pricing detail to update.
        updated_pricing_detail (PricingDetailIn): The updated pricing detail details.
        pricing_detail_service (IPricingDetailService, optional): The service for updating pricing detail data.

    Raises:
        HTTPException: 404 if the pricing detail does not exist.

    Returns:
        dict: The updated pricing detail details.
    """
    if await pricing_detail_service.get_by_id(pricing_detail_id=pricing_detail_id):
        await pricing_detail_service.update_pricing_detail(
            pricing_detail_id=pricing_detail_id,
            data=updated_pricing_detail,
        )
        return {**updated_pricing_detail.model_dump(), "id": pricing_detail_id}

    raise HTTPException(status_code=404, detail="PricingDetail not found")


@router.delete("/{pricing_detail_id}", status_code=204)
@inject
async def delete_pricing_detail(
        pricing_detail_id: int,
        pricing_detail_service: IPricingDetailService = Depends(Provide[Container.pricing_detail_service]),
) -> None:
    """
    Delete a pricing detail.

    Args:
        pricing_detail_id (int): The ID of the pricing detail to delete.
        pricing_detail_service (IPricingDetailService, optional): The service for managing pricing detail data.

    Raises:
        HTTPException: 404 if the pricing detail does not exist.
    """
    if not await pricing_detail_service.get_by_id(pricing_detail_id=pricing_detail_id):
        raise HTTPException(status_code=404, detail="PricingDetail not found")

    await pricing_detail_service.delete_pricing_detail(pricing_detail_id)

    return
