"""Module containing bill service abstractions."""

from abc import ABC, abstractmethod
from typing import List

from hotel_management_system.core.domains.bill import Bill, BillIn


class IBillService(ABC):
    """A class representing bill repository."""

    @abstractmethod
    async def get_all(self) -> List[Bill]:
        """The abstract getting all bills from the data storage.

        Returns:
            List[Bill]: Guests in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, room_id: int, pricing_detail_id: int) -> Bill | None:
        """The method getting bill by provided id.

        Args:
            room_id (int): The id of the room
            pricing_detail_id (int): The id of the accessibility_option.

        Returns:
            billDTO | None: The bill details.
        """

    @abstractmethod
    async def get_by_room_id(self, room_id: int) -> List[Bill] | None:
        """The method getting bill by provided room_id.

        Args:
            room_id (int): The id of the room

        Returns:
            Bill | None: The bill details.
        """

    @abstractmethod
    async def get_by_pricing_detail_id(self, pricing_detail_id: int) -> List[Bill] | None:
        """The method getting bill's by provided pricing_detail id.

        Args:
            pricing_detail_id (int): The id of the pricing_detail

        Returns:
            Bill | None: The bill details.
        """

    @abstractmethod
    async def get_by_reservation_id(self, reservation_id: int) -> List[Bill] | None:
        """The method getting bill's by provided pricing_detail id.

        Args:
            reservation_id (int): The id of the reservation

        Returns:
            Bill | None: The bill details.
        """

    @abstractmethod
    async def add_bill(self, data: BillIn) -> Bill | None:
        """The abstract adding new bill to the data storage.

        Args:
            data (GuestIn): The details of the new bill.

        Returns:
            Bill | None: The newly added bill.
        """

    @abstractmethod
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
            Bill | None: The updated bill details.
        """

    @abstractmethod
    async def delete_bill(self, room_id: int, pricing_detail_id: int) -> bool:
        """The abstract updating removing bill from the data storage.

        Args:
            room_id (int): The id of the room
            pricing_detail_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
        """