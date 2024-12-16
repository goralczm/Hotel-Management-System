"""Module containing guest_accessibility_option repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select

from hotel_management_system.core.repositories.i_guest_accessibility_option_repository import IGuestAccessibilityOptionRepository
from hotel_management_system.core.domains.guest_accessibility_option import GuestAccessibilityOption, GuestAccessibilityOptionIn
from hotel_management_system.db import (
    guests_accessibility_options_table,
    database,
)


class GuestAccessibilityOptionRepository(IGuestAccessibilityOptionRepository):
    """A class representing continent DB repository."""

    async def get_all_guest_accessibility_options(self) -> Iterable[Any]:
        """The method getting all guest_accessibility_options from the data storage.

        Returns:
            Iterable[Any]: guest_accessibility_options in the data storage.
        """

        query = (
            select(guests_accessibility_options_table)
        )
        guest_accessibility_options = await database.fetch_all(query)

        return [GuestAccessibilityOption.from_record(guest_accessibility_option) for guest_accessibility_option in guest_accessibility_options]

    async def get_by_id(self, guest_id: int, accessibility_option_id: int) -> Iterable[Any] | None:
        """The method getting guest_accessibility_option by provided id.

        Args:
            guest_id (int): The id of the guest
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            Any | None: The guest_accessibility_option details.
        """
        guest_accessibility_option = await self._get_by_id(guest_id, accessibility_option_id)

        return GuestAccessibilityOption.from_record(guest_accessibility_option) if guest_accessibility_option else None

    async def get_by_guest_id(self, guest_id: int) -> Iterable[GuestAccessibilityOption] | None:
        """The method getting guest_accessibility_option by provided guest_id.

        Args:
            guest_id (int): The id of the guest

        Returns:
            ReservationRoom | None: The accessibility_option_guest details.
        """

        query = (
            select(guests_accessibility_options_table).
            where(guests_accessibility_options_table.c.guest_id == guest_id)
        )
        guest_accessibility_options = await database.fetch_all(query)

        return [GuestAccessibilityOption.from_record(guest_accessibility_option) for guest_accessibility_option in guest_accessibility_options]

    async def get_by_accessibility_option_id(self, accessibility_option_id: int) -> Iterable[GuestAccessibilityOption] | None:
        """The method getting guest_accessibility_option's by provided accessibility_option id.

        Args:
            accessibility_option_id (int): The id of the accessibility_option

        Returns:
            ReservationRoom | None: The accessibility_option_guest details.
        """

        query = (
            select(guests_accessibility_options_table).
            where(guests_accessibility_options_table.c.accessibility_option_id == accessibility_option_id)
        )
        guest_accessibility_options = await database.fetch_all(query)

        return [GuestAccessibilityOption.from_record(guest_accessibility_option) for guest_accessibility_option in guest_accessibility_options]


    async def add_guest_accessibility_option(self, data: GuestAccessibilityOptionIn) -> Any | None:
        """The method adding new guest_accessibility_option to the data storage.

        Args:
            data (guest_accessibility_optionIn): The details of the new guest_accessibility_option.

        Returns:
            guest_accessibility_option: Full details of the newly added guest_accessibility_option.

        Returns:
            Any | None: The newly added guest_accessibility_option.
        """

        query = guests_accessibility_options_table.insert().values(**data.model_dump())
        await database.execute(query)

        return await self.get_by_id(data.guest_id, data.accessibility_option_id)

    async def update_guest_accessibility_option(
            self,
            guest_id: int,
            accessibility_option_id: int,
            data: GuestAccessibilityOptionIn,
    ) -> Any | None:
        """The abstract updating guest_accessibility_option data in the data storage.

        Args:
            guest_id (int): The id of the guest.
            accessibility_option_id (int): The id of the accessibility_option.
            data (GuestIn): The details of the updated guest_accessibility_option.

        Returns:
            Any | None: The updated guest_accessibility_option details.
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
        """The abstract updating removing guest_accessibility_option from the data storage.

        Args:
            guest_id (int): The id of the guest
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
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
            Any | None: guest_accessibility_option record if exists.
        """

        query = (
            guests_accessibility_options_table.select()
            .where(guests_accessibility_options_table.c.guest_id == guest_id and
                   guests_accessibility_options_table.c.accessibility_option_id == accessibility_option_id)
        )

        return await database.fetch_one(query)
