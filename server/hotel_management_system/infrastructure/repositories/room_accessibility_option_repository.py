"""
Module containing room_accessiblity_option repository implementation.
"""

from typing import List

from asyncpg import Record
from sqlalchemy import select

from hotel_management_system.core.repositories.i_room_accessibility_option_repository import \
    IRoomAccessibilityOptionRepository
from hotel_management_system.core.domains.room_accessibility_option import RoomAccessibilityOption, \
    RoomAccessibilityOptionIn
from hotel_management_system.db import (
    rooms_accessibility_options_table,
    database,
)


class RoomAccessibilityOptionRepository(IRoomAccessibilityOptionRepository):
    """
    A class representing room_accessibility_option DB repository.
    """

    async def get_all_room_accessibility_options(self) -> List[RoomAccessibilityOption]:
        """
        Retrieve all room accessibility options from the data storage.

        Returns:
            List[RoomAccessibilityOption]: A list of all room accessibility options.
        """

        query = (
            select(rooms_accessibility_options_table)
        )
        room_accessibility_options = await database.fetch_all(query)

        return [RoomAccessibilityOption.from_record(room_accessibility_option) for room_accessibility_option in
                room_accessibility_options]

    async def get_by_id(self, room_id: int, accessibility_option_id: int) -> RoomAccessibilityOption | None:
        """
        Retrieve a room accessibility option by its unique room ID and accessibility option ID.

        Args:
            room_id (int): The ID of the room.
            accessibility_option_id (int): The ID of the accessibility option.

        Returns:
            RoomAccessibilityOption | None: The room accessibility option details if found, or None if not found.
        """

        room_accessibility_option = await self._get_by_id(room_id, accessibility_option_id)

        return RoomAccessibilityOption.from_record(room_accessibility_option) if room_accessibility_option else None

    async def get_by_room_id(self, room_id: int) -> List[RoomAccessibilityOption]:
        """
        Retrieve room accessibility options for a specific room ID.

        Args:
            room_id (int): The ID of the room.

        Returns:
            RoomAccessibilityOption | None: The room accessibility option details if found
        """

        query = (
            rooms_accessibility_options_table.select()
            .where(rooms_accessibility_options_table.c.room_id == room_id)
        )

        rooms_accessibility_options = await database.fetch_all(query)

        return [RoomAccessibilityOption.from_record(rooms_accessibility_option) for rooms_accessibility_option in
                rooms_accessibility_options]

    async def add_room_accessibility_option(self, data: RoomAccessibilityOptionIn) -> RoomAccessibilityOption | None:
        """
        Add a new room accessibility option to the data storage.

        Args:
            data (RoomAccessibilityOption): The details of the new room accessibility option.

        Returns:
            RoomAccessibilityOption | None: The newly added room accessibility option, or None if the operation fails.
        """

        query = rooms_accessibility_options_table.insert().values(**data.model_dump())
        await database.execute(query)

        return await self.get_by_id(data.room_id, data.accessibility_option_id)

    async def update_room_accessibility_option(
            self,
            room_id: int,
            accessibility_option_id: int,
            data: RoomAccessibilityOptionIn,
    ) -> RoomAccessibilityOption | None:
        """
        Update the details of an existing room accessibility option in the data storage.

        Args:
            room_id (int): The ID of the room.
            accessibility_option_id (int): The ID of the accessibility option.
            data (RoomAccessibilityOption): The updated details for the room accessibility option.

        Returns:
            RoomAccessibilityOption | None: The updated room accessibility option details, or None if not found.
        """

        if self._get_by_id(room_id, accessibility_option_id):
            query = (
                rooms_accessibility_options_table.update()
                .where(rooms_accessibility_options_table.c.room_id == room_id and
                       rooms_accessibility_options_table.c.accessibility_option_id == accessibility_option_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            room_accessibility_option = await self._get_by_id(room_id, accessibility_option_id)

            return RoomAccessibilityOption(**dict(room_accessibility_option)) if room_accessibility_option else None

        return None

    async def delete_room_accessibility_option(self, room_id: int, accessibility_option_id: int) -> bool:
        """
        Remove a room accessibility option from the data storage.

        Args:
            room_id (int): The ID of the room.
            accessibility_option_id (int): The ID of the accessibility option.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """

        if self._get_by_id(room_id, accessibility_option_id):
            query = rooms_accessibility_options_table \
                .delete() \
                .where(rooms_accessibility_options_table.c.room_id == room_id and
                       rooms_accessibility_options_table.c.accessibility_option_id == accessibility_option_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, room_id: int, accessibility_option_id: int) -> Record | None:
        """A private method getting room_accessibility_option from the DB based on its ID.

        Args:
            room_id (int): The ID of the room
            accessibility_option_id (int): The ID of the accessibility_option.

        Returns:
            RoomAccessibilityOption | None: room_accessibility_option record if exists.
        """

        query = (
            rooms_accessibility_options_table.select()
            .where(rooms_accessibility_options_table.c.room_id == room_id and
                   rooms_accessibility_options_table.c.accessibility_option_id == accessibility_option_id)
        )

        return await database.fetch_one(query)
