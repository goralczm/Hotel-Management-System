"""Module containing guest repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select

from hotel_management_system.core.repositories.i_guest_repository import IGuestRepository
from hotel_management_system.core.domains.guest import Guest, GuestIn
from hotel_management_system.db import (
    guests_table,
    database,
)


class GuestRepository(IGuestRepository):
    """A class representing continent DB repository."""

    async def get_all_guests(self) -> Iterable[Any]:
        """The method getting all guests from the data storage.

        Returns:
            Iterable[Any]: guests in the data storage.
        """

        query = (
            select(guests_table)
            .order_by(guests_table.c.first_name.asc())
        )
        guests = await database.fetch_all(query)

        return [Guest.from_record(guest) for guest in guests]

    async def get_by_id(self, guest_id: int) -> Any | None:
        """The method getting guest by provided id.

        Args:
            guest_id (int): The id of the guest.

        Returns:
            Any | None: The guest details.
        """

        return await self._get_by_id(guest_id)

    async def add_guest(self, data: GuestIn) -> Any | None:
        """The method adding new guest to the data storage.

        Args:
            data (guestIn): The details of the new guest.

        Returns:
            guest: Full details of the newly added guest.

        Returns:
            Any | None: The newly added guest.
        """

        query = guests_table.insert().values(**data.model_dump())
        new_guest_id = await database.execute(query)
        new_guest = await self._get_by_id(new_guest_id)

        return Guest(**dict(new_guest)) if new_guest else None

    async def update_guest(
            self,
            guest_id: int,
            data: GuestIn,
    ) -> Any | None:
        """The method updating guest data in the data storage.

        Args:
            guest_id (int): The id of the guest.
            data (guestIn): The details of the updated guest.

        Returns:
            Any | None: The updated guest details.
        """

        if self._get_by_id(guest_id):
            query = (
                guests_table.update()
                .where(guests_table.c.id == guest_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            guest = await self._get_by_id(guest_id)

            return Guest(**dict(guest)) if guest else None

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
            Any | None: guest record if exists.
        """

        query = (
            guests_table.select()
            .where(guests_table.c.id == guest_id)
            .order_by(guests_table.c.first_name.asc())
        )

        return await database.fetch_one(query)
