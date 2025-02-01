"""
Module containing bill repository implementation.
"""

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
    """
    A class representing bill DB repository.
    """

    async def get_all_bills(self) -> Iterable[Any]:
        """
        Retrieve all bills from the data storage.

        Returns:
            List[Bill]: A list of all bills in the data storage.
        """

        query = (
            select(bills_table)
        )
        bills = await database.fetch_all(query)

        return [Bill.from_record(bill) for bill in bills]

    async def get_by_id(self, room_id: int, pricing_detail_id: int) -> Any | None:
        """
        Retrieve a bill by the specified room and pricing detail IDs.

        Args:
            room_id (int): The ID of the room.
            pricing_detail_id (int): The ID of the pricing detail.

        Returns:
            Bill | None: The bill details if found, or None if not found.
        """

        bill = await self._get_by_id(room_id, pricing_detail_id)

        return Bill.from_record(bill) if bill else None

    async def get_by_room_id(self, room_id: int) -> Any | None:
        """
        Retrieve all bills associated with the specified room ID.

        Args:
            room_id (int): The ID of the room.

        Returns:
            List[Bill] | None: A list of bills for the specified room, or None if not found.
        """

        query = (
            bills_table.select()
            .where(bills_table.c.room_id == room_id)
        )

        bill = await database.fetch_one(query)

        return Bill.from_record(bill) if bill else None

    async def get_by_pricing_detail_id(self, pricing_detail_id: int) -> Any | None:
        """
        Retrieve all bills associated with the specified pricing detail ID.

        Args:
            pricing_detail_id (int): The ID of the pricing detail.

        Returns:
            List[Bill] | None: A list of bills for the specified pricing detail, or None if not found.
        """

        query = (
            select(bills_table).
            where(bills_table.c.pricing_detail_id == pricing_detail_id)
        )

        bills = await database.fetch_all(query)

        return [Bill.from_record(bill) for bill in bills]

    async def get_by_reservation_id(self, reservation_id: int) -> List[Bill] | None:
        """
        Retrieve all bills associated with the specified reservation ID.

        Args:
            reservation_id (int): The ID of the reservation.

        Returns:
            List[Bill] | None: A list of bills for the specified reservation, or None if not found.
        """

        query = (
            select(bills_table).
            where(bills_table.c.reservation_id == reservation_id)
        )

        bills = await database.fetch_all(query)

        return [Bill.from_record(bill) for bill in bills]

    async def add_bill(self, data: BillIn) -> Any | None:
        """
        Add a new bill to the data storage.

        Args:
            data (BillIn): The details of the new bill.

        Returns:
            Bill | None: The newly added bill, or None if the operation fails.
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
        """
        Update an existing bill in the data storage.

        Args:
            room_id (int): The ID of the room.
            pricing_detail_id (int): The ID of the pricing detail.
            data (BillIn): The updated data for the bill.

        Returns:
            Bill | None: The updated bill details, or None if not found.
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
        """
        Remove a bill from the data storage.

        Args:
            room_id (int): The ID of the room.
            pricing_detail_id (int): The ID of the pricing detail.

        Returns:
            bool: True if the operation is successful, False otherwise.
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
