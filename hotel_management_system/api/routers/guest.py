"""A module containing continent endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from hotel_management_system.container import Container
from hotel_management_system.core.domains.guest import Guest, GuestIn
from hotel_management_system.infrastructure.dtos.guestdto import GuestDTO
from hotel_management_system.infrastructure.services.iguestservice import IGuestService

router = APIRouter()


@router.post("/create", response_model=Guest, status_code=201)
@inject
async def create_guest(
        guest: GuestIn,
        service: IGuestService = Depends(Provide[Container.guest_service]),
) -> dict:
    """An endpoint for adding new guest.

    Args:
        guest (GuestIn): The guest data.
        service (IGuestService, optional): The injected service dependency.

    Returns:
        dict: The new guest attributes.
    """

    new_guest = await service.add_guest(guest)

    return new_guest.model_dump() if new_guest else {}


@router.get("/all", response_model=Iterable[GuestDTO], status_code=200)
@inject
async def get_all_guests(
        service: IGuestService = Depends(Provide[Container.guest_service]),
) -> Iterable:
    """An endpoint for getting all guests.

    Args:
        service (IGuestService, optional): The injected service dependency.

    Returns:
        Iterable: The guest attributes collection.
    """

    guests = await service.get_all()

    return guests


@router.get(
    "/{guest_id}",
    response_model=GuestDTO,
    status_code=200,
)
@inject
async def get_guest_by_id(
        guest_id: int,
        service: IGuestService = Depends(Provide[Container.guest_service]),
) -> dict | None:
    """An endpoint for getting guest by id.

    Args:
        guest_id (int): The id of the guest.
        service (IGuestService, optional): The injected service dependency.

    Returns:
        dict | None: The guest details.
    """

    if guest := await service.get_by_id(guest_id):
        return guest.model_dump()

    raise HTTPException(status_code=404, detail="Guest not found")


@router.put("/{guest_id}", response_model=Guest, status_code=201)
@inject
async def update_guest(
        guest_id: int,
        updated_guest: GuestIn,
        service: IGuestService = Depends(Provide[Container.guest_service]),
) -> dict:
    """An endpoint for updating guest data.

    Args:
        guest_id (int): The id of the guest.
        updated_guest (GuestIn): The updated guest details.
        service (IGuesttService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if guest does not exist.

    Returns:
        dict: The updated guest details.
    """

    if await service.get_by_id(guest_id=guest_id):
        await service.update_guest(
            guest_id=guest_id,
            data=updated_guest,
        )
        return {**updated_guest.model_dump(), "id": guest_id}

    raise HTTPException(status_code=404, detail="Guest not found")


@router.delete("/{guest_id}", status_code=204)
@inject
async def delete_guest(
        guest_id: int,
        service: IGuestService = Depends(Provide[Container.guest_service]),
) -> None:
    """An endpoint for deleting guests.

    Args:
        guest_id (int): The id of the guest.
        service (IcontinentService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if guest does not exist.
    """

    if await service.get_by_id(guest_id=guest_id):
        await service.delete_guest(guest_id)

        return

    raise HTTPException(status_code=404, detail="Guest not found")