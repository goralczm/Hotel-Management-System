"""
Module containing bill service implementation.
"""

from typing import List

from hotel_management_system.core.domains.bill import Bill, BillIn
from hotel_management_system.core.repositories.i_bill_repository import IBillRepository
from hotel_management_system.core.repositories.i_pricing_detail_repository import IPricingDetailRepository
from hotel_management_system.core.services.i_bill_service import IBillService


class BillService(IBillService):
    """
    A class implementing the bill service.
    """

    _bill_repository: IBillRepository
    _pricing_detail_repository: IPricingDetailRepository

    def __init__(self,
                 bill_repository: IBillRepository,
                 pricing_detail_repository: IPricingDetailRepository,
                 ) -> None:
        """
        The initializer of the `bill service`.

        Args:
            bill_repository (IBillRepository): The reference to the bill repository
            pricing_detail_repository (IPricingDetailRepository): The reference to the pricing_detail repository
        """

        self._bill_repository = bill_repository
        self._pricing_detail_repository = pricing_detail_repository

    async def get_all(self) -> List[Bill]:
        """
        Retrieve all bills from the data storage.

        Returns:
            List[Bill]: A list of all bills in the data storage.
        """

        all_bills = await self._bill_repository.get_all_bills()

        return [await self.parse_bill(bill) for bill in all_bills]

    async def get_by_id(self, room_id: int, pricing_detail_id: int) -> Bill | None:
        """
        Retrieve a bill by the specified room and pricing detail IDs.

        Args:
            room_id (int): The ID of the room.
            pricing_detail_id (int): The ID of the pricing detail.

        Returns:
            Bill | None: The bill details if found, or None if not found.
        """

        return await self.parse_bill(
            await self._bill_repository.get_by_id(room_id, pricing_detail_id)
        )

    async def get_by_room_id(self, room_id: int) -> List[Bill] | None:
        """
        Retrieve all bills associated with the specified room ID.

        Args:
            room_id (int): The ID of the room.

        Returns:
            List[Bill] | None: A list of bills for the specified room, or None if not found.
        """

        all_bills = await self._bill_repository.get_by_room_id(room_id)

        return [await self.parse_bill(bill) for bill in all_bills]

    async def get_by_pricing_detail_id(self, pricing_detail_id: int) -> List[Bill] | None:
        """
        Retrieve all bills associated with the specified pricing detail ID.

        Args:
            pricing_detail_id (int): The ID of the pricing detail.

        Returns:
            List[Bill] | None: A list of bills for the specified pricing detail, or None if not found.
        """

        all_bills = await self._bill_repository.get_by_pricing_detail_id(pricing_detail_id)

        return [await self.parse_bill(bill) for bill in all_bills]

    async def get_by_reservation_id(self, reservation_id: int) -> List[Bill] | None:
        """
        Retrieve all bills associated with the specified reservation ID.

        Args:
            reservation_id (int): The ID of the reservation.

        Returns:
            List[Bill] | None: A list of bills for the specified reservation, or None if not found.
        """

        all_bills = await self._bill_repository.get_by_reservation_id(reservation_id)

        return [await self.parse_bill(bill) for bill in all_bills]

    async def add_bill(self, data: BillIn) -> Bill | None:
        """
        Add a new bill to the data storage.

        Args:
            data (BillIn): The details of the new bill.

        Returns:
            Bill | None: The newly added bill, or None if the operation fails.
        """

        return await self.parse_bill(
            await self._bill_repository.add_bill(data)
        )

    async def update_bill(
            self,
            room_id: int,
            pricing_detail_id: int,
            data: BillIn,
    ) -> Bill | None:
        """
        Update an existing bill in the data storage.

        Args:
            room_id (int): The ID of the room.
            pricing_detail_id (int): The ID of the pricing detail.
            data (BillIn): The updated data for the bill.

        Returns:
            Bill | None: The updated bill details, or None if not found.
        """

        return await self.parse_bill(
            await self._bill_repository.update_bill(
                room_id=room_id,
                pricing_detail_id=pricing_detail_id,
                data=data,
            )
        )

    async def delete_bill(self, room_id: int, pricing_detail_id: int) -> bool:
        """
        Remove a bill from the data storage.

        Args:
            room_id (int): The ID of the room.
            pricing_detail_id (int): The ID of the pricing detail.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """

        return await self._bill_repository.delete_bill(room_id, pricing_detail_id)

    async def parse_bill(self, bill: Bill) -> Bill:
        if bill:
            pricing_detail = await self._pricing_detail_repository.get_by_id(bill.pricing_detail_id)

            bill.pricing_detail = pricing_detail

        return bill
