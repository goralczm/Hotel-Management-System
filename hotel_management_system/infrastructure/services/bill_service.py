"""Module containing continent service implementation."""

from typing import Iterable, List

from hotel_management_system.core.domains.bill import Bill, BillIn
from hotel_management_system.core.repositories.i_bill_repository import IBillRepository
from hotel_management_system.core.repositories.i_pricing_detail_repository import IPricingDetailRepository
from hotel_management_system.core.services.i_bill_service import IBillService


class BillService(IBillService):
    """A class implementing the bill service."""

    _bill_repository: IBillRepository
    _pricing_detail_repository: IPricingDetailRepository

    def __init__(self,
                 bill_repository: IBillRepository,
                 pricing_detail_repository: IPricingDetailRepository,
                 ) -> None:
        """The initializer of the `bill service`.

        Args:
            bill_repository (IbillRepository): The reference to the repository.
        """

        self._bill_repository = bill_repository
        self._pricing_detail_repository = pricing_detail_repository

    async def get_all(self) -> Iterable[Bill]:
        """The method getting all bills from the repository.

        Returns:
            Iterable[billDTO]: All bills.
        """

        all_bills = await self._bill_repository.get_all_bills()

        return [await self.parse_bill(bill) for bill in all_bills]

    async def get_by_id(self, room_id: int, pricing_detail_id: int) -> Bill | None:
        """The method getting bill by provided id.

        Args:
            room_id (int): The id of the room
            pricing_detail_id (int): The id of the accessibility_option.

        Returns:
            billDTO | None: The bill details.
        """

        return await self.parse_bill(
            await self._bill_repository.get_by_id(room_id, pricing_detail_id)
        )

    async def get_by_room_id(self, room_id: int) -> List[Bill] | None:
        """The method getting bill by provided room_id.

        Args:
            room_id (int): The id of the room

        Returns:
            Bill | None: The bill details.
        """

        all_bills = await self._bill_repository.get_by_room_id(room_id)

        return [await self.parse_bill(bill) for bill in all_bills]

    async def get_by_pricing_detail_id(self, pricing_detail_id: int) -> List[Bill] | None:
        """The method getting bill's by provided pricing_detail id.

        Args:
            pricing_detail_id (int): The id of the pricing_detail

        Returns:
            Bill | None: The bill details.
        """

        all_bills = await self._bill_repository.get_by_pricing_detail_id(pricing_detail_id)

        return [await self.parse_bill(bill) for bill in all_bills]

    async def get_by_reservation_id(self, reservation_id: int) -> List[Bill] | None:
        """The method getting bill's by provided pricing_detail id.

        Args:
            reservation_id (int): The id of the reservation

        Returns:
            Bill | None: The bill details.
        """

        all_bills = await self._bill_repository.get_by_reservation_id(reservation_id)

        return [await self.parse_bill(bill) for bill in all_bills]

    async def add_bill(self, data: BillIn) -> Bill | None:
        """The method adding new bill to the data storage.

        Args:
            data (billIn): The details of the new bill.

        Returns:
            bill | None: Full details of the newly added bill.
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
        """The abstract updating bill data in the data storage.

        Args:
            room_id (int): The id of the room.
            pricing_detail_id (int): The id of the accessibility_option.
            data (GuestIn): The details of the updated bill.

        Returns:
            Any | None: The updated bill details.
        """

        return await self.parse_bill(
            await self._bill_repository.update_bill(
                room_id=room_id,
                pricing_detail_id=pricing_detail_id,
                data=data,
            )
        )

    async def delete_bill(self, room_id: int, pricing_detail_id: int) -> bool:
        """The abstract updating removing bill from the data storage.

        Args:
            room_id (int): The id of the room
            pricing_detail_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
        """

        return await self._bill_repository.delete_bill(room_id, pricing_detail_id)

    async def parse_bill(self, bill: Bill) -> Bill:
        if bill:
            pricing_detail = await self._pricing_detail_repository.get_by_id(bill.pricing_detail_id)

            bill.pricing_detail = pricing_detail

        return bill
