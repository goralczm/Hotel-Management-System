"""
Module containing accessibility_option repository implementation.
"""

from typing import List

from asyncpg import Record  # type: ignore
from sqlalchemy import select

from hotel_management_system.core.repositories.i_accessibility_option_repository import IAccessibilityOptionRepository
from hotel_management_system.core.domains.accessibility_option import AccessibilityOption, AccessibilityOptionIn
from hotel_management_system.db import (
    accessibility_options_table,
    database,
)


class AccessibilityOptionRepository(IAccessibilityOptionRepository):
    """
    A class representing accessibility_option DB repository.
    """

    async def get_all_accessibility_options(self) -> List[AccessibilityOption]:
        """
        Retrieve all accessibility options from the data storage.

        Returns:
            List[AccessibilityOption]: A collection of all accessibility options.
        """

        query = (
            select(accessibility_options_table)
            .order_by(accessibility_options_table.c.name.asc())
        )
        accessibility_options = await database.fetch_all(query)

        return [AccessibilityOption.from_record(accessibility_option) for accessibility_option in accessibility_options]

    async def add_accessibility_option(self, data: AccessibilityOptionIn) -> AccessibilityOption | None:
        """
        Add a new accessibility option to the data storage.

        Args:
            data (AccessibilityOptionIn): The data for the new accessibility option.

        Returns:
            AccessibilityOption | None: The newly added accessibility option, or None if the operation fails.
        """

        query = accessibility_options_table.insert().values(**data.model_dump())
        new_accessibility_option_id = await database.execute(query)
        new_accessibility_option = await self._get_by_id(new_accessibility_option_id)

        return AccessibilityOption(**dict(new_accessibility_option)) if new_accessibility_option else None

    async def get_by_id(self, accessibility_option_id: int) -> AccessibilityOption | None:
        """
        Retrieve an accessibility option by its ID.

        Args:
            accessibility_option_id (int): The ID of the accessibility option.

        Returns:
            AccessibilityOption | None: The accessibility option details, or None if not found.
        """

        accessibility_option = await self._get_by_id(accessibility_option_id)

        return AccessibilityOption.from_record(accessibility_option) if accessibility_option else None

    async def get_by_name(self, accessibility_option_name: str) -> AccessibilityOption | None:
        """
        Retrieve an accessibility option by its name.

        Args:
            accessibility_option_name (str): The name of the accessibility option.

        Returns:
            AccessibilityOption | None: The accessibility option details, or None if not found.
        """

        query = (
            accessibility_options_table.select()
            .where(accessibility_options_table.c.name == accessibility_option_name)
        )

        return await database.fetch_one(query)

    async def update_accessibility_option(
            self,
            accessibility_option_id: int,
            data: AccessibilityOptionIn,
    ) -> AccessibilityOption | None:
        """
        Update an existing accessibility option in the data storage.

        Args:
            accessibility_option_id (int): The ID of the accessibility option to update.
            data (AccessibilityOptionIn): The updated data for the accessibility option.

        Returns:
            AccessibilityOption | None: The updated accessibility option, or None if not found.
        """

        if self._get_by_id(accessibility_option_id):
            query = (
                accessibility_options_table.update()
                .where(accessibility_options_table.c.id == accessibility_option_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            accessibility_option = await self._get_by_id(accessibility_option_id)

            return AccessibilityOption(**dict(accessibility_option)) if accessibility_option else None

        return None

    async def delete_accessibility_option(self, accessibility_option_id: int) -> bool:
        """
        Remove an accessibility option from the data storage.

        Args:
            accessibility_option_id (int): The ID of the accessibility option to delete.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """

        if self._get_by_id(accessibility_option_id):
            query = accessibility_options_table \
                .delete() \
                .where(accessibility_options_table.c.id == accessibility_option_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, accessibility_option_id: int) -> Record | None:
        """A private method getting accessibility_option from the DB based on its ID.

        Args:
            accessibility_option_id (int): The ID of the accessibility_option.

        Returns:
            Record | None: accessibility_option record if exists.
        """

        query = (
            accessibility_options_table.select()
            .where(accessibility_options_table.c.id == accessibility_option_id)
            .order_by(accessibility_options_table.c.name.asc())
        )

        return await database.fetch_one(query)
