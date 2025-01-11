"""Module containing reservation repository implementation."""
from datetime import date
from typing import Any, Iterable, List

from asyncpg import Record  # type: ignore
from sqlalchemy import select, extract

from hotel_management_system.core.repositories.i_reservation_repository import IReservationRepository
from hotel_management_system.core.domains.reservation import Reservation, ReservationIn
from hotel_management_system.db import (
    reservations_table,
    reservation_rooms_table,
    database,
)


class ReservationRepository(IReservationRepository):
    """A class representing continent DB repository."""

    async def get_all_reservations(self) -> List[Reservation]:
        """The method getting all reservations from the data storage.

        Returns:
            Iterable[Any]: reservations in the data storage.
        """

        query = (
            select(reservations_table)
            .order_by(reservations_table.c.start_date.asc())
        )

        reservations = await database.fetch_all(query)

        return [Reservation.from_record(reservation) for reservation in reservations]

    async def get_by_id(self, reservation_id: int) -> Reservation | None:
        """The method getting reservation by provided id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            reservationDTO | None: The reservation details.
        """
        reservation = await self._get_by_id(reservation_id)

        return Reservation.from_record(reservation) if reservation else None

    async def get_by_month(self, year: int, month_number: int) -> List[Reservation]:
        """The method getting reservations made in the provided month

        Args:
            month_number (int): The month number

        Returns:
            List[Reservation]: The reservations made in provided month
        """

        query = (
            select(reservations_table)
            .filter(extract('year', reservations_table.c.start_date) == year)
            .filter(extract('month', reservations_table.c.start_date) == month_number)
        )

        reservations = await database.fetch_all(query)

        return [Reservation.from_record(reservation) for reservation in reservations]

    async def get_between_dates(self, start_date: date, end_date: date) -> List[Reservation]:
        """The method getting reservations made between provided start_date and end_date

        Args:
            start_date (date): The start date
            end_date (date): The end date

        Returns:
            List[Reservation]: The reservations made between the dates
        """

        query = (
            select(reservations_table)
            .filter(reservations_table.c.start_date.between(start_date, end_date))
        )

        reservations = await database.fetch_all(query)

        return [Reservation.from_record(reservation) for reservation in reservations]


    async def add_reservation(self, data: ReservationIn) -> Any | None:
        """The method adding new reservation to the data storage.

        Args:
            data (reservationIn): The details of the new reservation.

        Returns:
            reservation: Full details of the newly added reservation.

        Returns:
            Any | None: The newly added reservation.
        """

        query = reservations_table.insert().values(**data.model_dump())
        new_reservation_id = await database.execute(query)

        return await self._get_by_id(new_reservation_id)

    async def update_reservation(
            self,
            reservation_id: int,
            data: ReservationIn,
    ) -> Any | None:
        """The method updating reservation data in the data storage.

        Args:
            reservation_id (int): The id of the reservation.
            data (reservationIn): The details of the updated reservation.

        Returns:
            Any | None: The updated reservation details.
        """

        if self._get_by_id(reservation_id):
            query = (
                reservations_table.update()
                .where(reservations_table.c.id == reservation_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            return await self.get_by_id(reservation_id)

        return None

    async def delete_reservation(self, reservation_id: int) -> bool:
        """The method updating removing reservation from the data storage.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(reservation_id):
            query = reservations_table \
                .delete() \
                .where(reservations_table.c.id == reservation_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, reservation_id: int) -> Record | None:
        """A private method getting reservation from the DB based on its ID.

        Args:
            reservation_id (int): The ID of the reservation.

        Returns:
            Any | None: reservation record if exists.
        """

        query = (
            reservations_table.select()
            .where(reservations_table.c.id == reservation_id)
        )

        return await database.fetch_one(query)
