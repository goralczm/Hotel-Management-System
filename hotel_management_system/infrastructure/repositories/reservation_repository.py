"""Module containing reservation repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select

from hotel_management_system.core.repositories.i_reservation_repository import IReservationRepository
from hotel_management_system.core.domains.reservation import Reservation, ReservationIn
from hotel_management_system.db import (
    reservations_table,
    database,
)


class ReservationRepository(IReservationRepository):
    """A class representing continent DB repository."""

    async def get_all_reservations(self) -> Iterable[Any]:
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
        new_reservation = await self._get_by_id(new_reservation_id)

        return Reservation(**dict(new_reservation)) if new_reservation else None

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

            reservation = await self._get_by_id(reservation_id)

            return Reservation(**dict(reservation)) if reservation else None

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
