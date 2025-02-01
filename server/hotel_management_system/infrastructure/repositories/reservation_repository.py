"""
Module containing reservation repository implementation.
"""

from datetime import date
from typing import List

from asyncpg import Record
from sqlalchemy import select, extract

from hotel_management_system.core.repositories.i_reservation_repository import IReservationRepository
from hotel_management_system.core.domains.reservation import Reservation, ReservationIn
from hotel_management_system.db import (
    reservations_table,
    database,
)


class ReservationRepository(IReservationRepository):
    """
    A class representing reservation DB repository.
    """

    async def get_all_reservations(self) -> List[Reservation]:
        """
        Retrieve all reservations from the data storage.

        Returns:
            List[Reservation]: A list of all reservations.
        """

        query = (
            select(reservations_table)
            .order_by(reservations_table.c.start_date.asc())
        )

        reservations = await database.fetch_all(query)

        return [Reservation.from_record(reservation) for reservation in reservations]

    async def get_by_id(self, reservation_id: int) -> Reservation | None:
        """
        Retrieve a reservation by its unique ID.

        Args:
            reservation_id (int): The ID of the reservation.

        Returns:
            Reservation | None: The details of the reservation if found, or None if not found.
        """

        reservation = await self._get_by_id(reservation_id)

        return Reservation.from_record(reservation) if reservation else None

    async def get_by_month(self, year: int, month_number: int) -> List[Reservation]:
        """
        Retrieve reservations made during the specified month.

        Args:
            year (int): The year of the reservations.
            month_number (int): The month number (1 for January, 12 for December).

        Returns:
            List[Reservation]: A list of reservations made in the specified month.
        """

        query = (
            select(reservations_table)
            .filter(extract('year', reservations_table.c.start_date) == year)
            .filter(extract('month', reservations_table.c.start_date) == month_number)
        )

        reservations = await database.fetch_all(query)

        return [Reservation.from_record(reservation) for reservation in reservations]

    async def get_between_dates(self, start_date: date, end_date: date) -> List[Reservation]:
        """
        Retrieve reservations made between the provided start and end dates.

        Args:
            start_date (date): The start date of the range.
            end_date (date): The end date of the range.

        Returns:
            List[Reservation]: A list of reservations made within the date range.
        """

        query = (
            select(reservations_table)
            .filter(reservations_table.c.start_date.between(start_date, end_date))
        )

        reservations = await database.fetch_all(query)

        return [Reservation.from_record(reservation) for reservation in reservations]

    async def add_reservation(self, data: ReservationIn) -> Reservation | None:
        """
        Add a new reservation to the data storage.

        Args:
            data (ReservationIn): The details of the new reservation.

        Returns:
            Reservation | None: The newly added reservation, or None if the operation fails.
        """

        query = reservations_table.insert().values(**data.model_dump())
        new_reservation_id = await database.execute(query)

        return await self._get_by_id(new_reservation_id)

    async def update_reservation(
            self,
            reservation_id: int,
            data: ReservationIn,
    ) -> Reservation | None:
        """
        Update the details of an existing reservation in the data storage.

        Args:
            reservation_id (int): The ID of the reservation to update.
            data (ReservationIn): The updated details for the reservation.

        Returns:
            Reservation | None: The updated reservation details, or None if the reservation is not found.
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
        """
        Remove a reservation from the data storage.

        Args:
            reservation_id (int): The ID of the reservation to remove.

        Returns:
            bool: True if the operation is successful, False otherwise.
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
            Reservation | None: reservation record if exists.
        """

        query = (
            reservations_table.select()
            .where(reservations_table.c.id == reservation_id)
        )

        return await database.fetch_one(query)
