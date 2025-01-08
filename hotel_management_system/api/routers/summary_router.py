from typing import Iterable, List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from hotel_management_system.core.domains.reservation import Reservation
from hotel_management_system.core.services.i_reservation_service import IReservationService
from hotel_management_system.container import Container

router = APIRouter()


@router.get("/monthly/{month_number}", response_model=dict, status_code=201)
@inject
async def montly_summary(
        month_number: int,
        reservation_service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> dict:
    monthly_reservations = await reservation_service.get_by_month(month_number)
    return {
        "reserved_rooms": len(monthly_reservations),
        "total_cost": sum([reservation.get_cost() for reservation in monthly_reservations]),
        "total_guests": sum([reservation.number_of_guests for reservation in monthly_reservations]),
    }
