"""
Module containing guest repository implementation.
"""

from typing import List

from asyncpg import Record
from sqlalchemy import select

from hotel_management_system.core.repositories.i_guest_repository import IGuestRepository
from hotel_management_system.core.domains.guest import Guest, GuestIn
from hotel_management_system.db import (
    guests_table,
    database,
)


class GuestRepository(IGuestRepository):
    """
    A class representing guest DB repository.
    """

    async def get_all_guests(self) -> List[Guest]:
        """
        Retrieve all guests from the data storage.

        Returns:
            List[Guest]: A list of all guests.
        """

        query = (
            select(guests_table)
            .order_by(guests_table.c.first_name.asc())
        )
        guests = await database.fetch_all(query)

        return [Guest.from_record(guest) for guest in guests]

    async def get_by_id(self, guest_id: int) -> Guest | None:
        """
        Retrieve a guest by their unique ID.

        Args:
            guest_id (int): The ID of the guest.

        Returns:
            Guest | None: The details of the guest if found, or None if not found.
        """

        guest = await self._get_by_id(guest_id)

        return Guest.from_record(guest) if guest else None

    async def get_by_first_name(self, first_name: str) -> List[Guest] | None:
        """
        Retrieve guests by their first name.

        Args:
            first_name (str): The first name of the guest(s).

        Returns:
            List[Guest] | None: A list of guests matching the first name, or None if no match is found.
        """


        query = (
            guests_table.select()
            .where(guests_table.c.first_name == first_name)
        )

        guests = await database.fetch_all(query)

        return [Guest.from_record(guest) for guest in guests]

    async def get_by_last_name(self, last_name: str) -> List[Guest] | None:
        """
        Retrieve guests by their last name.

        Args:
            last_name (str): The last name of the guest(s).

        Returns:
            List[Guest] | None: A list of guests matching the last name, or None if no match is found.
        """

        query = (
            guests_table.select()
            .where(guests_table.c.last_name == last_name)
        )

        guests = await database.fetch_all(query)

        return [Guest.from_record(guest) for guest in guests]

    async def get_by_needle_in_name(self, needle: str) -> List[Guest] | None:
        """
        Search for guests whose names contain a specific substring.

        Args:
            needle (str): A substring to search for within guest names.

        Returns:
            List[Guest] | None: A list of guests whose names contain the substring, or None if no match is found.
        """

        needle = needle.lower()

        query = (
            guests_table.select()
            .where(guests_table.c.first_name.ilike(f'%{needle}%') | guests_table.c.last_name.ilike(f'%{needle}%'))
        )

        guests = await database.fetch_all(query)

        return [Guest.from_record(guest) for guest in guests]

    async def add_guest(self, data: GuestIn) -> Guest | None:
        """
        Add a new guest to the data storage.

        Args:
            data (GuestIn): The details of the new guest.

        Returns:
            Guest | None: The newly added guest, or None if the operation fails.
        """

        query = guests_table.insert().values(**data.model_dump())
        new_guest_id = await database.execute(query)

        return await self.get_by_id(new_guest_id)

    async def update_guest(
            self,
            guest_id: int,
            data: GuestIn,
    ) -> Guest | None:
        """
        Update an existing guest's data in the data storage.

        Args:
            guest_id (int): The ID of the guest to update.
            data (GuestIn): The updated details for the guest.

        Returns:
            Guest | None: The updated guest details, or None if the guest is not found.
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
        """
        Remove a guest from the data storage.

        Args:
            guest_id (int): The ID of the guest to remove.

        Returns:
            bool: True if the operation is successful, False otherwise.
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
