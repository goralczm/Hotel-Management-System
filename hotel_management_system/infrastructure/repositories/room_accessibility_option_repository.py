"""Module containing room_accessibility_option repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select

from hotel_management_system.core.repositories.i_room_accessibility_option_repository import IRoomAccessibilityOptionRepository
from hotel_management_system.core.domains.room_accessibility_option import RoomAccessibilityOption, RoomAccessibilityOptionIn
from hotel_management_system.db import (
    rooms_accessibility_options_table,
    database,
)


class RoomAccessibilityOptionRepository(IRoomAccessibilityOptionRepository):
    """A class representing continent DB repository."""

    async def get_all_room_accessibility_options(self) -> Iterable[Any]:
        """The method getting all room_accessibility_options from the data storage.

        Returns:
            Iterable[Any]: room_accessibility_options in the data storage.
        """

        query = (
            select(rooms_accessibility_options_table)
        )
        room_accessibility_options = await database.fetch_all(query)

        return [RoomAccessibilityOption.from_record(room_accessibility_option) for room_accessibility_option in room_accessibility_options]

    async def get_by_id(self, room_id: int, accessibility_option_id: int) -> Any | None:
        """The method getting room_accessibility_option by provided id.

        Args:
            room_id (int): The id of the room
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            Any | None: The room_accessibility_option details.
        """
        room_accessibility_option = await self._get_by_id(room_id, accessibility_option_id)

        return RoomAccessibilityOption.from_record(room_accessibility_option) if room_accessibility_option else None

    async def add_room_accessibility_option(self, data: RoomAccessibilityOptionIn) -> Any | None:
        """The method adding new room_accessibility_option to the data storage.

        Args:
            data (room_accessibility_optionIn): The details of the new room_accessibility_option.

        Returns:
            room_accessibility_option: Full details of the newly added room_accessibility_option.

        Returns:
            Any | None: The newly added room_accessibility_option.
        """

        query = rooms_accessibility_options_table.insert().values(**data.model_dump())
        await database.execute(query)

        return await self.get_by_id(data.room_id, data.accessibility_option_id)

    async def update_room_accessibility_option(
            self,
            room_id: int,
            accessibility_option_id: int,
            data: RoomAccessibilityOptionIn,
    ) -> Any | None:
        """The abstract updating room_accessibility_option data in the data storage.

        Args:
            room_id (int): The id of the room.
            accessibility_option_id (int): The id of the accessibility_option.
            data (GuestIn): The details of the updated room_accessibility_option.

        Returns:
            Any | None: The updated room_accessibility_option details.
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
        """The abstract updating removing room_accessibility_option from the data storage.

        Args:
            room_id (int): The id of the room
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
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
            Any | None: room_accessibility_option record if exists.
        """

        query = (
            rooms_accessibility_options_table.select()
            .where(rooms_accessibility_options_table.c.room_id == room_id and
                   rooms_accessibility_options_table.c.accessibility_option_id == accessibility_option_id)
        )

        return await database.fetch_one(query)
