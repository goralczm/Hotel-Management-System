"""Module containing reservation_room repository implementation."""

from typing import Any, Iterable, List

from asyncpg import Record  # type: ignore
from sqlalchemy import select

from hotel_management_system.core.repositories.i_reservation_room_repository import IReservationRoomRepository
from hotel_management_system.core.domains.reservation_room import ReservationRoom, ReservationRoomIn
from hotel_management_system.db import (
    reservation_rooms_table,
    database,
)


class ReservationRoomRepository(IReservationRoomRepository):
    """A class representing continent DB repository."""

    async def get_all_reservation_rooms(self) -> Iterable[Any]:
        """The method getting all reservation_rooms from the data storage.

        Returns:
            Iterable[Any]: reservation_rooms in the data storage.
        """

        query = (
            select(reservation_rooms_table)
        )
        reservation_rooms = await database.fetch_all(query)

        return [ReservationRoom.from_record(reservation_room) for reservation_room in reservation_rooms]

    async def get_by_id(self, room_id: int, reservation_id: int) -> Any | None:
        """The method getting reservation_room by provided id.

        Args:
            room_id (int): The id of the room
            reservation_id (int): The id of the accessibility_option.

        Returns:
            Any | None: The reservation_room details.
        """
        reservation_room = await self._get_by_id(room_id, reservation_id)

        return ReservationRoom.from_record(reservation_room) if reservation_room else None

    async def get_by_room_id(self, room_id: int) -> List[ReservationRoom] | None:
        """The method getting reservation_room by provided room_id.

        Args:
            room_id (int): The id of the room

        Returns:
            ReservationRoom | None: The reservation_room details.
        """

        query = (
            select(reservation_rooms_table)
            .where(reservation_rooms_table.c.room_id == room_id)
        )

        reservation_rooms = await database.fetch_all(query)

        return [ReservationRoom.from_record(reservation_room) for reservation_room in reservation_rooms]

    async def get_by_reservation_id(self, reservation_id: int) -> Any | None:
        """The method getting reservation_room's by provided reservation id.

        Args:
            reservation_id (int): The id of the reservation

        Returns:
            ReservationRoom | None: The reservation_room details.
        """

        query = (
            select(reservation_rooms_table).
            where(reservation_rooms_table.c.reservation_id == reservation_id)
        )
        reservation_rooms = await database.fetch_all(query)

        return [ReservationRoom.from_record(reservation_room) for reservation_room in reservation_rooms]

    async def add_reservation_room(self, data: ReservationRoomIn) -> Any | None:
        """The method adding new reservation_room to the data storage.

        Args:
            data (reservation_roomIn): The details of the new reservation_room.

        Returns:
            reservation_room: Full details of the newly added reservation_room.

        Returns:
            Any | None: The newly added reservation_room.
        """

        query = reservation_rooms_table.insert().values(**data.model_dump())
        await database.execute(query)

        return await self.get_by_id(data.room_id, data.reservation_id)

    async def update_reservation_room(
            self,
            room_id: int,
            reservation_id: int,
            data: ReservationRoomIn,
    ) -> Any | None:
        """The abstract updating reservation_room data in the data storage.

        Args:
            room_id (int): The id of the room.
            reservation_id (int): The id of the accessibility_option.
            data (GuestIn): The details of the updated reservation_room.

        Returns:
            Any | None: The updated reservation_room details.
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
        """The abstract updating removing reservation_room from the data storage.

        Args:
            room_id (int): The id of the room
            reservation_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
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
            Any | None: reservation_room record if exists.
        """

        query = (
            reservation_rooms_table.select()
            .where(reservation_rooms_table.c.room_id == room_id and
                   reservation_rooms_table.c.reservation_id == reservation_id)
        )

        return await database.fetch_one(query)
