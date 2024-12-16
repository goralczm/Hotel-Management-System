"""Module containing bill repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable, List

from hotel_management_system.core.domains.bill import BillIn, Bill


class IBillRepository(ABC):
    """An abstract class representing protocol of continent repository."""

    @abstractmethod
    async def get_all_bills(self) -> Iterable[Any]:
        """The abstract getting all bills from the data storage.

        Returns:
            Iterable[Any]: Guests in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, room_id: int, pricing_detail_id: int) -> Any | None:
        """The method getting bill by provided id.

        Args:
            room_id (int): The id of the room
            pricing_detail_id (int): The id of the accessibility_option.

        Returns:
            billDTO | None: The bill details.
        """

    @abstractmethod
    async def get_by_room_id(self, room_id: int) -> Any | None:
        """The method getting bill by provided room_id.

        Args:
            room_id (int): The id of the room

        Returns:
            Bill | None: The bill details.
        """

    @abstractmethod
    async def get_by_pricing_detail_id(self, pricing_detail_id: int) -> Any | None:
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
    async def add_bill(self, data: BillIn) -> Any | None:
        """The abstract adding new bill to the data storage.

        Args:
            data (GuestIn): The details of the new bill.

        Returns:
            Any | None: The newly added bill.
        """

    @abstractmethod
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

    @abstractmethod
    async def delete_bill(self, room_id: int, pricing_detail_id: int) -> bool:
        """The abstract updating removing bill from the data storage.

        Args:
            room_id (int): The id of the room
            pricing_detail_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
        """
