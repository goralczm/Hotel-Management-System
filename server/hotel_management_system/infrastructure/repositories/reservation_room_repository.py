"""
Module containing reservation_room repository implementation.
"""

from typing import List

from asyncpg import Record
from sqlalchemy import select

from hotel_management_system.core.repositories.i_reservation_room_repository import IReservationRoomRepository
from hotel_management_system.core.domains.reservation_room import ReservationRoom, ReservationRoomIn
from hotel_management_system.db import (
    reservation_rooms_table,
    database,
)


class ReservationRoomRepository(IReservationRoomRepository):
    """
    A class representing reservation_room DB repository.
    """

    async def get_all_reservation_rooms(self) -> List[ReservationRoom]:
        """
        Retrieve all reservation rooms from the data storage.

        Returns:
            List[ReservationRoom]: A list of all reservation rooms.
        """

        query = (
            select(reservation_rooms_table)
        )
        reservation_rooms = await database.fetch_all(query)

        return [ReservationRoom.from_record(reservation_room) for reservation_room in reservation_rooms]

    async def get_by_id(self, room_id: int, reservation_id: int) -> ReservationRoom | None:
        """
        Retrieve a reservation room by its unique room ID and reservation ID.

        Args:
            room_id (int): The ID of the room.
            reservation_id (int): The ID of the reservation.

        Returns:
            List[ReservationRoom] | None: The reservation room details if found, or None if not found.
        """

        reservation_room = await self._get_by_id(room_id, reservation_id)

        return ReservationRoom.from_record(reservation_room) if reservation_room else None

    async def get_by_room_id(self, room_id: int) -> List[ReservationRoom] | None:
        """
        Retrieve reservation rooms for a specific room ID.

        Args:
            room_id (int): The ID of the room.

        Returns:
            List[ReservationRoom] | None: The reservation rooms for the specified room, or None if no rooms are found.
        """

        query = (
            select(reservation_rooms_table)
            .where(reservation_rooms_table.c.room_id == room_id)
        )

        reservation_rooms = await database.fetch_all(query)

        return [ReservationRoom.from_record(reservation_room) for reservation_room in reservation_rooms]

    async def get_by_reservation_id(self, reservation_id: int) -> List[ReservationRoom]:
        """
        Retrieve a reservation room by its reservation ID.

        Args:
            reservation_id (int): The ID of the reservation.

        Returns:
            ReservationRoom | None: The reservation room details if found
        """

        query = (
            select(reservation_rooms_table).
            where(reservation_rooms_table.c.reservation_id == reservation_id)
        )
        reservation_rooms = await database.fetch_all(query)

        return [ReservationRoom.from_record(reservation_room) for reservation_room in reservation_rooms]

    async def add_reservation_room(self, data: ReservationRoomIn) -> ReservationRoom | None:
        """
        Add a new reservation room to the data storage.

        Args:
            data (ReservationRoomIn): The details of the new reservation room.

        Returns:
            ReservationRoom | None: The newly added reservation room, or None if the operation fails.
        """

        query = reservation_rooms_table.insert().values(**data.model_dump())
        await database.execute(query)

        return await self.get_by_id(data.room_id, data.reservation_id)

    async def update_reservation_room(
            self,
            room_id: int,
            reservation_id: int,
            data: ReservationRoomIn,
    ) -> ReservationRoom | None:
        """
        Update the details of an existing reservation room in the data storage.

        Args:
            room_id (int): The ID of the room.
            reservation_id (int): The ID of the reservation.
            data (ReservationRoomIn): The updated details for the reservation room.

        Returns:
            ReservationRoom | None: The updated reservation room details, or None if the reservation room is not found.
        """

        if self._get_by_id(room_id, reservation_id):
            query = (
                reservation_rooms_table.update()
                .where(reservation_rooms_table.c.room_id == room_id and
                       reservation_rooms_table.c.reservation_id == reservation_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            reservation_room = await self._get_by_id(room_id, reservation_id)

            return ReservationRoom(**dict(reservation_room)) if reservation_room else None

        return None

    async def delete_reservation_room(self, room_id: int, reservation_id: int) -> bool:
        """
        Remove a reservation room from the data storage.

        Args:
            room_id (int): The ID of the room.
            reservation_id (int): The ID of the reservation.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """


        if self._get_by_id(room_id, reservation_id):
            query = reservation_rooms_table \
                .delete() \
                .where(reservation_rooms_table.c.room_id == room_id and
                       reservation_rooms_table.c.reservation_id == reservation_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, room_id: int, reservation_id: int) -> Record | None:
        """A private method getting reservation_room from the DB based on its ID.

        Args:
            room_id (int): The ID of the room
            reservation_id (int): The ID of the accessibility_option.

        Returns:
            ReservationRoom | None: reservation_room record if exists.
        """

        query = (
            reservation_rooms_table.select()
            .where(reservation_rooms_table.c.room_id == room_id and
                   reservation_rooms_table.c.reservation_id == reservation_id)
        )

        return await database.fetch_one(query)
