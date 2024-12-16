"""Module containing bill repository implementation."""

from typing import Any, Iterable, List

from asyncpg import Record  # type: ignore
from sqlalchemy import select

from hotel_management_system.core.repositories.i_bill_repository import IBillRepository
from hotel_management_system.core.domains.bill import Bill, BillIn
from hotel_management_system.db import (
    bills_table,
    database,
)


class BillRepository(IBillRepository):
    """A class representing continent DB repository."""

    async def get_all_bills(self) -> Iterable[Any]:
        """The method getting all bills from the data storage.

        Returns:
            Iterable[Any]: bills in the data storage.
        """

        query = (
            select(bills_table)
        )
        bills = await database.fetch_all(query)

        return [Bill.from_record(bill) for bill in bills]

    async def get_by_id(self, room_id: int, pricing_detail_id: int) -> Any | None:
        """The method getting bill by provided id.

        Args:
            room_id (int): The id of the room
            pricing_detail_id (int): The id of the accessibility_option.

        Returns:
            Any | None: The bill details.
        """
        bill = await self._get_by_id(room_id, pricing_detail_id)

        return Bill.from_record(bill) if bill else None

    async def get_by_room_id(self, room_id: int) -> Any | None:
        """The method getting bill by provided room_id.

        Args:
            room_id (int): The id of the room

        Returns:
            Bill | None: The bill details.
        """

        query = (
            bills_table.select()
            .where(bills_table.c.room_id == room_id)
        )

        bill = await database.fetch_one(query)

        return Bill.from_record(bill) if bill else None

    async def get_by_pricing_detail_id(self, pricing_detail_id: int) -> Any | None:
        """The method getting bill's by provided pricing_detail id.

        Args:
            pricing_detail_id (int): The id of the pricing_detail

        Returns:
            Bill | None: The bill details.
        """

        query = (
            select(bills_table).
            where(bills_table.c.pricing_detail_id == pricing_detail_id)
        )

        bills = await database.fetch_all(query)

        return [Bill.from_record(bill) for bill in bills]

    async def get_by_reservation_id(self, reservation_id: int) -> List[Bill] | None:
        """The method getting bill's by provided pricing_detail id.

        Args:
            reservation_id (int): The id of the reservation

        Returns:
            Bill | None: The bill details.
        """

        query = (
            select(bills_table).
            where(bills_table.c.reservation_id == reservation_id)
        )

        bills = await database.fetch_all(query)

        return [Bill.from_record(bill) for bill in bills]

    async def add_bill(self, data: BillIn) -> Any | None:
        """The method adding new bill to the data storage.

        Args:
            data (billIn): The details of the new bill.

        Returns:
            bill: Full details of the newly added bill.

        Returns:
            Any | None: The newly added bill.
        """

        query = bills_table.insert().values(**data.model_dump())
        await database.execute(query)

        return await self.get_by_id(data.room_id, data.pricing_detail_id)

    async def update_bill(
            self,
            room_id: int,
            pricing_detail_id: int,
            data: BillIn,
    ) -> Any | None:
        """The abstract updating bill data in the data storage.

        Args:
            room_id (int): The id of the room.
            pricing_detail_id (int): The id of the accessibility_option.
            data (GuestIn): The details of the updated bill.

        Returns:
            Any | None: The updated bill details.
        """

        if self._get_by_id(room_id, pricing_detail_id):
            query = (
                bills_table.update()
                .where(bills_table.c.room_id == room_id and
                       bills_table.c.pricing_detail_id == pricing_detail_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            bill = await self._get_by_id(room_id, pricing_detail_id)

            return Bill(**dict(bill)) if bill else None

        return None

    async def delete_bill(self, room_id: int, pricing_detail_id: int) -> bool:
        """The abstract updating removing bill from the data storage.

        Args:
            room_id (int): The id of the room
            pricing_detail_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(room_id, pricing_detail_id):
            query = bills_table \
                .delete() \
                .where(bills_table.c.room_id == room_id and
                       bills_table.c.pricing_detail_id == pricing_detail_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, room_id: int, pricing_detail_id: int) -> Record | None:
        """A private method getting bill from the DB based on its ID.

        Args:
            room_id (int): The ID of the room
            pricing_detail_id (int): The ID of the accessibility_option.

        Returns:
            Any | None: bill record if exists.
        """

        query = (
            bills_table.select()
            .where(bills_table.c.room_id == room_id and
                   bills_table.c.pricing_detail_id == pricing_detail_id)
        )

        return await database.fetch_one(query)
