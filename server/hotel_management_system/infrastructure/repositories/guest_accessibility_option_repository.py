"""
Module containing guest_accessibility_option repository implementation.
"""

from typing import List

from asyncpg import Record
from sqlalchemy import select

from hotel_management_system.core.repositories.i_guest_accessibility_option_repository import IGuestAccessibilityOptionRepository
from hotel_management_system.core.domains.guest_accessibility_option import GuestAccessibilityOption, GuestAccessibilityOptionIn
from hotel_management_system.db import (
    guests_accessibility_options_table,
    database,
)


class GuestAccessibilityOptionRepository(IGuestAccessibilityOptionRepository):
    """
    A class representing guest_accessiblity_option DB repository.
    """

    async def get_all_guest_accessibility_options(self) -> List[GuestAccessibilityOption]:
        """
        Retrieve all guest accessibility options from the data storage.

        Returns:
            List[GuestAccessibilityOption]: A collection of all guest accessibility options.
        """

        query = (
            select(guests_accessibility_options_table)
        )
        guest_accessibility_options = await database.fetch_all(query)

        return [GuestAccessibilityOption.from_record(guest_accessibility_option) for guest_accessibility_option in guest_accessibility_options]

    async def get_by_id(self, guest_id: int, accessibility_option_id: int) -> List[GuestAccessibilityOption] | None:
        """
        Retrieve a guest accessibility option by guest ID and accessibility option ID.

        Args:
            guest_id (int): The ID of the guest.
            accessibility_option_id (int): The ID of the accessibility option.

        Returns:
            GuestAccessibilityOption | None: The details of the guest accessibility option if found
        """

        guest_accessibility_option = await self._get_by_id(guest_id, accessibility_option_id)

        return GuestAccessibilityOption.from_record(guest_accessibility_option) if guest_accessibility_option else None

    async def get_by_guest_id(self, guest_id: int) -> List[GuestAccessibilityOption] | None:
        """
        Retrieve all accessibility options associated with a specific guest ID.

        Args:
            guest_id (int): The ID of the guest.

        Returns:
            List[GuestAccessibilityOption]: A collection of guest accessibility options if found
        """

        query = (
            select(guests_accessibility_options_table).
            where(guests_accessibility_options_table.c.guest_id == guest_id)
        )
        guest_accessibility_options = await database.fetch_all(query)

        return [GuestAccessibilityOption.from_record(guest_accessibility_option) for guest_accessibility_option in guest_accessibility_options]

    async def get_by_accessibility_option_id(self, accessibility_option_id: int) -> List[GuestAccessibilityOption] | None:
        """
        Retrieve all guest accessibility options associated with a specific accessibility option ID.

        Args:
            accessibility_option_id (int): The ID of the accessibility option.

        Returns:
            List[GuestAccessibilityOption]: A collection of guest accessibility options if found
        """

        query = (
            select(guests_accessibility_options_table).
            where(guests_accessibility_options_table.c.accessibility_option_id == accessibility_option_id)
        )

        guest_accessibility_options = await database.fetch_all(query)

        return [GuestAccessibilityOption.from_record(guest_accessibility_option) for guest_accessibility_option in guest_accessibility_options]

    async def add_guest_accessibility_option(self, data: GuestAccessibilityOptionIn) -> GuestAccessibilityOption | None:
        """
        Add a new guest accessibility option to the data storage.

        Args:
            data (GuestAccessibilityOptionIn): The details of the new guest accessibility option.

        Returns:
            GuestAccessibilityOption | None: The newly added guest accessibility option, or None if the operation fails.
        """

        query = guests_accessibility_options_table.insert().values(**data.model_dump())
        await database.execute(query)

        return await self.get_by_id(data.guest_id, data.accessibility_option_id)

    async def update_guest_accessibility_option(
            self,
            guest_id: int,
            accessibility_option_id: int,
            data: GuestAccessibilityOptionIn,
    ) -> GuestAccessibilityOption | None:
        """
        Update an existing guest accessibility option in the data storage.

        Args:
            guest_id (int): The ID of the guest.
            accessibility_option_id (int): The ID of the accessibility option.
            data (GuestAccessibilityOptionIn): The updated data for the guest accessibility option.

        Returns:
            GuestAccessibilityOption | None: The updated guest accessibility option, or None if not found.
        """

        if self._get_by_id(guest_id, accessibility_option_id):
            query = (
                guests_accessibility_options_table.update()
                .where(guests_accessibility_options_table.c.guest_id == guest_id and
                       guests_accessibility_options_table.c.accessibility_option_id == accessibility_option_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            guest_accessibility_option = await self._get_by_id(guest_id, accessibility_option_id)

            return GuestAccessibilityOption(**dict(guest_accessibility_option)) if guest_accessibility_option else None

        return None

    async def delete_guest_accessibility_option(self, guest_id: int, accessibility_option_id: int) -> bool:
        """
        Remove a guest accessibility option from the data storage.

        Args:
            guest_id (int): The ID of the guest.
            accessibility_option_id (int): The ID of the accessibility option.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """

        if self._get_by_id(guest_id, accessibility_option_id):
            query = guests_accessibility_options_table \
                .delete() \
                .where(guests_accessibility_options_table.c.guest_id == guest_id and
                       guests_accessibility_options_table.c.accessibility_option_id == accessibility_option_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, guest_id: int, accessibility_option_id: int) -> Record | None:
        """A private method getting guest_accessibility_option from the DB based on its ID.

        Args:
            guest_id (int): The ID of the guest
            accessibility_option_id (int): The ID of the accessibility_option.

        Returns:
            GuestAccessibilityOption | None: guest_accessibility_option record if exists.
        """

        query = (
            guests_accessibility_options_table.select()
            .where(guests_accessibility_options_table.c.guest_id == guest_id and
                   guests_accessibility_options_table.c.accessibility_option_id == accessibility_option_id)
        )

        return await database.fetch_one(query)
