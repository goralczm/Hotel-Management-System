"""
Module for managing bill service abstractions.
"""

from abc import ABC, abstractmethod
from typing import List

from hotel_management_system.core.domains.bill import Bill, BillIn


class IBillService(ABC):
    """A class representing bill repository."""

    @abstractmethod
    async def get_all(self) -> List[Bill]:
        """
        Retrieve all bills from the data storage.

        Returns:
            List[Bill]: A list of all bills in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, room_id: int, pricing_detail_id: int) -> Bill | None:
        """
        Retrieve a bill by the specified room and pricing detail IDs.

        Args:
            room_id (int): The ID of the room.
            pricing_detail_id (int): The ID of the pricing detail.

        Returns:
            Bill | None: The bill details if found, or None if not found.
        """

    @abstractmethod
    async def get_by_room_id(self, room_id: int) -> List[Bill] | None:
        """
        Retrieve all bills associated with the specified room ID.

        Args:
            room_id (int): The ID of the room.

        Returns:
            List[Bill] | None: A list of bills for the specified room, or None if not found.
        """

    @abstractmethod
    async def get_by_pricing_detail_id(self, pricing_detail_id: int) -> List[Bill] | None:
        """
        Retrieve all bills associated with the specified pricing detail ID.

        Args:
            pricing_detail_id (int): The ID of the pricing detail.

        Returns:
            List[Bill] | None: A list of bills for the specified pricing detail, or None if not found.
        """

    @abstractmethod
    async def get_by_reservation_id(self, reservation_id: int) -> List[Bill] | None:
        """
        Retrieve all bills associated with the specified reservation ID.

        Args:
            reservation_id (int): The ID of the reservation.

        Returns:
            List[Bill] | None: A list of bills for the specified reservation, or None if not found.
        """

    @abstractmethod
    async def add_bill(self, data: BillIn) -> Bill | None:
        """
        Add a new bill to the data storage.

        Args:
            data (BillIn): The details of the new bill.

        Returns:
            Bill | None: The newly added bill, or None if the operation fails.
        """

    @abstractmethod
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

    @abstractmethod
    async def delete_bill(self, room_id: int, pricing_detail_id: int) -> bool:
        """
        Remove a bill from the data storage.

        Args:
            room_id (int): The ID of the room.
            pricing_detail_id (int): The ID of the pricing detail.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """