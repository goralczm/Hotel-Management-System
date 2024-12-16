"""A module containing continent endpoints."""

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
    """An endpoint for adding new pricing_detail.

    Args:
        pricing_detail (PricingDetailIn): The pricing_detail data.
        pricing_detail_service (IPricingDetailService, optional): The injected service dependency.

    Returns:
        dict: The new pricing_detail attributes.
    """

    new_pricing_detail = await pricing_detail_service.add_pricing_detail(pricing_detail)

    return new_pricing_detail.model_dump() if new_pricing_detail else {}


@router.get("/all", response_model=Iterable[PricingDetail], status_code=200)
@inject
async def get_all_pricing_details(
        pricing_detail_service: IPricingDetailService = Depends(Provide[Container.pricing_detail_service]),
) -> Iterable:
    """An endpoint for getting all pricing_details.

    Args:
        pricing_detail_service (IPricingDetailService, optional): The injected service dependency.

    Returns:
        Iterable: The pricing_detail attributes collection.
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
    """An endpoint for getting pricing_detail by id.

    Args:
        pricing_detail_id (int): The id of the pricing_detail.
        pricing_detail_service (IPricingDetailService, optional): The injected service dependency.

    Returns:
        dict | None: The pricing_detail details.
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
    """An endpoint for updating pricing_detail data.

    Args:
        pricing_detail_id (int): The id of the pricing_detail.
        updated_pricing_detail (PricingDetailIn): The updated pricing_detail details.
        pricing_detail_service (IPricingDetailService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if pricing_detail does not exist.

    Returns:
        dict: The updated pricing_detail details.
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
    """An endpoint for deleting pricing_details.

    Args:
        pricing_detail_id (int): The id of the pricing_detail.
        pricing_detail_service (IPricingDetailService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if pricing_detail does not exist.
    """

    if not await pricing_detail_service.get_by_id(pricing_detail_id=pricing_detail_id):
        raise HTTPException(status_code=404, detail="PricingDetail not found")

    await pricing_detail_service.delete_pricing_detail(pricing_detail_id)

    return
