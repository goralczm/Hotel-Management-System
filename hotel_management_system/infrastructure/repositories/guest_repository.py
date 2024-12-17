"""Module containing guest repository implementation."""

from typing import List

from asyncpg import Record  # type: ignore
from sqlalchemy import select

from hotel_management_system.core.domains.accessibility_option import AccessibilityOption
from hotel_management_system.core.repositories.i_guest_repository import IGuestRepository
from hotel_management_system.core.domains.guest import Guest, GuestIn
from hotel_management_system.db import (
    guests_table,
    guests_accessibility_options_table,
    accessibility_options_table,
    database,
)


class GuestRepository(IGuestRepository):
    """A class representing continent DB repository."""

    async def get_all_guests(self) -> List[Guest]:
        """The method getting all guests from the data storage.

        Returns:
            List[Guest]: guests in the data storage.
        """

        query = (
            select(guests_table)
            .order_by(guests_table.c.first_name.asc())
        )
        guests = await database.fetch_all(query)

        return [await self.parse_record(guest) for guest in guests]

    async def get_by_id(self, guest_id: int) -> Guest | None:
        """The method getting guest by provided id.

        Args:
            guest_id (int): The id of the guest.

        Returns:
            Guest | None: The guest details.
        """

        return await self.parse_record(await self._get_by_id(guest_id))

    async def add_guest(self, data: GuestIn) -> Guest | None:
        """The method adding new guest to the data storage.

        Args:
            data (guestIn): The details of the new guest.

        Returns:
            guest: Full details of the newly added guest.

        Returns:
            Guest | None: The newly added guest.
        """

        query = guests_table.insert().values(**data.model_dump())
        new_guest_id = await database.execute(query)
        new_guest = await self._get_by_id(new_guest_id)

        return await self.parse_record(new_guest)

    async def update_guest(
            self,
            guest_id: int,
            data: GuestIn,
    ) -> Guest | None:
        """The method updating guest data in the data storage.

        Args:
            guest_id (int): The id of the guest.
            data (guestIn): The details of the updated guest.

        Returns:
            Guest | None: The updated guest details.
        """

        if self._get_by_id(guest_id):
            query = (
                guests_table.update()
                .where(guests_table.c.id == guest_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            return await self.get_by_id(guest_id)

        return None

    async def delete_guest(self, guest_id: int) -> bool:
        """The method updating removing guest from the data storage.

        Args:
            guest_id (int): The id of the guest.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(guest_id):
            query = guests_table \
                .delete() \
                .where(guests_table.c.id == guest_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, guest_id: int) -> Record | None:
        """A private method getting guest from the DB based on its ID.

        Args:
            guest_id (int): The ID of the guest.

        Returns:
            Guest | None: guest record if exists.
        """

        query = (
            guests_table.select()
            .where(guests_table.c.id == guest_id)
        )

        return await database.fetch_one(query)

    async def parse_record(self, guest_record: Record) -> Guest:
        result_dict = dict(guest_record)

        sub_query = (
            select(guests_accessibility_options_table)
            .where(guests_accessibility_options_table.c.guest_id == result_dict.get("id"))
        )

        sub_result = await database.fetch_all(sub_query)

        accessibility_options = []
        for guest_accessibility_option in sub_result:
            sub_sub_query = (
                select(accessibility_options_table)
                .where(accessibility_options_table.c.id == dict(guest_accessibility_option).get("accessibility_option_id"))
            )

            sub_sub_result = await database.fetch_one(sub_sub_query)

            accessibility_options.append(AccessibilityOption.from_record(sub_sub_result))

        new_guest = Guest.from_record(guest_record)
        new_guest.accessibility_options = accessibility_options

        return new_guest
