"""Module containing room repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select

from hotel_management_system.src.core.repositories.i_room_repository import IRoomRepository
from hotel_management_system.src.core.domains.room import Room, RoomIn
from hotel_management_system.src.db import (
    rooms_table,
    database,
)


class RoomRepository(IRoomRepository):
    """A class representing continent DB repository."""

    async def get_all_rooms(self) -> Iterable[Any]:
        """The method getting all rooms from the data storage.

        Returns:
            Iterable[Any]: rooms in the data storage.
        """

        query = (
            select(rooms_table)
            .order_by(rooms_table.c.alias.asc())
        )
        rooms = await database.fetch_all(query)

        return [Room.from_record(room) for room in rooms]

    async def get_by_id(self, room_id: int) -> Any | None:
        """The method getting room by provided id.

        Args:
            room_id (int): The id of the room.

        Returns:
            Any | None: The room details.
        """

        return await self._get_by_id(room_id)

    async def add_room(self, data: RoomIn) -> Any | None:
        """The method adding new room to the data storage.

        Args:
            data (roomIn): The details of the new room.

        Returns:
            room: Full details of the newly added room.

        Returns:
            Any | None: The newly added room.
        """

        query = rooms_table.insert().values(**data.model_dump())
        new_room_id = await database.execute(query)
        new_room = await self._get_by_id(new_room_id)

        return Room(**dict(new_room)) if new_room else None

    async def update_room(
            self,
            room_id: int,
            data: RoomIn,
    ) -> Any | None:
        """The method updating room data in the data storage.

        Args:
            room_id (int): The id of the room.
            data (roomIn): The details of the updated room.

        Returns:
            Any | None: The updated room details.
        """

        if self._get_by_id(room_id):
            query = (
                rooms_table.update()
                .where(rooms_table.c.id == room_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            room = await self._get_by_id(room_id)

            return Room(**dict(room)) if room else None

        return None

    async def delete_room(self, room_id: int) -> bool:
        """The method updating removing room from the data storage.

        Args:
            room_id (int): The id of the room.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(room_id):
            query = rooms_table \
                .delete() \
                .where(rooms_table.c.id == room_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, room_id: int) -> Record | None:
        """A private method getting room from the DB based on its ID.

        Args:
            room_id (int): The ID of the room.

        Returns:
            Any | None: room record if exists.
        """

        query = (
            rooms_table.select()
            .where(rooms_table.c.id == room_id)
            .order_by(rooms_table.c.alias.asc())
        )

        return await database.fetch_one(query)
