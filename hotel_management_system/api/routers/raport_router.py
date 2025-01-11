from typing import Iterable, List
from datetime import date, datetime

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from hotel_management_system.core.domains.reservation import Reservation
from hotel_management_system.core.services.i_reservation_service import IReservationService
from hotel_management_system.container import Container
from hotel_management_system.core.services.i_room_service import IRoomService

raport_router = APIRouter()


async def generate_raport(
        reservations: List[Reservation],
        room_service: IRoomService = Depends(Provide(Container.room_service)),
) -> dict:
    all_rooms = await room_service.get_all()

    return {
        "reserved_rooms_count": len(reservations),
        "free_rooms_count": len(all_rooms) - len(reservations),
        "total_income": sum([reservation.get_cost() for reservation in reservations]),
        "total_guests_count": sum([reservation.number_of_guests for reservation in reservations]),
        "total_guests_with_accessibilities_count": len([reservation.guest for reservation in reservations if
                                                        len(reservation.guest.accessibility_options) > 0])
    }


@raport_router.get("/date/{date}", response_model=dict, status_code=201)
@inject
async def date_raport(
        date: date,
        reservation_service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> dict:
    reservations = await reservation_service.get_between_dates(date, date)

    return await generate_raport(reservations)


@raport_router.get("/date/{start_date}/{end_date}", response_model=dict, status_code=201)
@inject
async def between_dates_raport(
        start_date: date,
        end_date: date,
        reservation_service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> dict:
    reservations = await reservation_service.get_between_dates(start_date, end_date)

    return await generate_raport(reservations)


@raport_router.get("/today", response_model=dict, status_code=201)
@inject
async def todays_raport(
        reservation_service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> dict:
    today = datetime.today()
    reservations = await reservation_service.get_between_dates(today, today)

    return await generate_raport(reservations)


@raport_router.get("/year/{year}", response_model=dict, status_code=201)
@inject
async def yearly_raport(
        year: int,
        reservation_service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> dict:
    reservations_this_month = await reservation_service.get_by_year(year)

    return await generate_raport(reservations_this_month)


@raport_router.get("/year/{year}/month/{month_number}", response_model=dict, status_code=201)
@inject
async def montly_raport(
        year: int,
        month_number: int,
        reservation_service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> dict:
    reservations_this_month = await reservation_service.get_by_month(year, month_number)

    return await generate_raport(reservations_this_month)
