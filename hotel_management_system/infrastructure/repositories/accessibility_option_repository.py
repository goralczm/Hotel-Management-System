"""Module containing accessibility_option repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select

from hotel_management_system.core.repositories.i_accessibility_option_repository import IAccessibilityOptionRepository
from hotel_management_system.core.domains.accessibility_option import AccessibilityOption, AccessibilityOptionIn
from hotel_management_system.db import (
    accessibility_options_table,
    database,
)


class AccessibilityOptionRepository(IAccessibilityOptionRepository):
    """A class representing continent DB repository."""

    async def get_all_accessibility_options(self) -> Iterable[Any]:
        """The method getting all accessibility_options from the data storage.

        Returns:
            Iterable[Any]: accessibility_options in the data storage.
        """

        query = (
            select(accessibility_options_table)
            .order_by(accessibility_options_table.c.name.asc())
        )
        accessibility_options = await database.fetch_all(query)

        return [AccessibilityOption.from_record(accessibility_option) for accessibility_option in accessibility_options]

    async def get_by_id(self, accessibility_option_id: int) -> Any | None:
        """The method getting accessibility_option by provided id.

        Args:
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            Any | None: The accessibility_option details.
        """
        accessibility_option = await self._get_by_id(accessibility_option_id)

        return AccessibilityOption.from_record(accessibility_option) if accessibility_option else None

    async def get_by_name(self, accessibility_option_name: str) -> AccessibilityOption | None:
        """The method getting accessibility_option by provided name.

        Args:
            accessibility_option_name (str): The name of the accessibility_option.

        Returns:
            accessibility_optionDTO | None: The accessibility_option details.
        """

        query = (
            accessibility_options_table.select()
            .where(accessibility_options_table.c.name == accessibility_option_name)
        )

        return await database.fetch_one(query)

    async def add_accessibility_option(self, data: AccessibilityOptionIn) -> Any | None:
        """The method adding new accessibility_option to the data storage.

        Args:
            data (accessibility_optionIn): The details of the new accessibility_option.

        Returns:
            accessibility_option: Full details of the newly added accessibility_option.

        Returns:
            Any | None: The newly added accessibility_option.
        """

        query = accessibility_options_table.insert().values(**data.model_dump())
        new_accessibility_option_id = await database.execute(query)
        new_accessibility_option = await self._get_by_id(new_accessibility_option_id)

        return AccessibilityOption(**dict(new_accessibility_option)) if new_accessibility_option else None

    async def update_accessibility_option(
            self,
            accessibility_option_id: int,
            data: AccessibilityOptionIn,
    ) -> Any | None:
        """The method updating accessibility_option data in the data storage.

        Args:
            accessibility_option_id (int): The id of the accessibility_option.
            data (accessibility_optionIn): The details of the updated accessibility_option.

        Returns:
            Any | None: The updated accessibility_option details.
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
        """The method updating removing accessibility_option from the data storage.

        Args:
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
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
            Any | None: accessibility_option record if exists.
        """

        query = (
            accessibility_options_table.select()
            .where(accessibility_options_table.c.id == accessibility_option_id)
            .order_by(accessibility_options_table.c.name.asc())
        )

        return await database.fetch_one(query)
