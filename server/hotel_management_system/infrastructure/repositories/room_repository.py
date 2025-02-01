"""
Module containing room repository implementation.
"""

from typing import List

from asyncpg import Record
from sqlalchemy import select

from hotel_management_system.core.repositories.i_room_repository import IRoomRepository
from hotel_management_system.core.domains.room import Room, RoomIn
from hotel_management_system.db import (
    rooms_table,
    database,
)


class RoomRepository(IRoomRepository):
    """
    A class representing room DB repository.
    """

    async def get_all_rooms(self) -> List[Room]:
        """
        Retrieve all rooms from the data storage.

        Returns:
            List[Room]: A list of all rooms stored in the database.
        """

        query = (
            select(rooms_table)
            .order_by(rooms_table.c.alias.asc())
        )

        rooms = await database.fetch_all(query)

        return [Room.from_record(room) for room in rooms]

    async def get_by_id(self, room_id: int) -> Room | None:
        """
        Retrieve a room by its unique ID.

        Args:
            room_id (int): The ID of the room.

        Returns:
            Room | None: The room details if found, or None if no room with the given ID exists.
        """

        room = await self._get_by_id(room_id)

        return Room.from_record(room) if room else None

    async def add_room(self, data: RoomIn) -> Room | None:
        """
        Add a new room to the data storage.

        Args:
            data (RoomIn): The details of the new room.

        Returns:
            Room | None: The newly added room if successful, or None if the operation fails.
        """

        query = rooms_table.insert().values(**data.model_dump())
        new_room_id = await database.execute(query)

        return await self.get_by_id(new_room_id)

    async def update_room(
            self,
            room_id: int,
            data: RoomIn,
    ) -> Room | None:
        """
        Update the details of an existing room in the data storage.

        Args:
            room_id (int): The ID of the room to update.
            data (RoomIn): The updated room details.

        Returns:
            Room | None: The updated room details if successful, or None if no room with the given ID exists.
        """

        if self._get_by_id(room_id):
            query = (
                rooms_table.update()
                .where(rooms_table.c.id == room_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            return await self.get_by_id(room_id)

        return None

    async def delete_room(self, room_id: int) -> bool:
        """
        Remove a room from the data storage.

        Args:
            room_id (int): The ID of the room to remove.

        Returns:
            bool: True if the operation was successful, False otherwise.
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
