"""Module containing guest repository abstractions."""

from abc import ABC, abstractmethod
from typing import List

from hotel_management_system.core.domains.guest import GuestIn, Guest


class IGuestRepository(ABC):
    """An abstract class representing protocol of continent repository."""

    @abstractmethod
    async def get_all_guests(self) -> List[Guest]:
        """The abstract getting all guests from the data storage.

        Returns:
            List[Guest]: Guests in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, guest_id: int) -> Guest | None:
        """The method getting guest by provided id.

        Args:
            guest_id (int): The id of the guest.

        Returns:
            guestDTO | None: The guest details.
        """

    @abstractmethod
    async def get_by_first_name(self, first_name: str) -> List[Guest] | None:
        """

        :param guest_name:
        :return:
        """

    @abstractmethod
    async def get_by_last_name(self, last_name: str) -> List[Guest] | None:
        """

        :param guest_name:
        :return:
        """

    @abstractmethod
    async def get_by_needle_in_name(self, needle: str) -> List[Guest] | None:
        """

        :param guest_name:
        :return:
        """

    @abstractmethod
    async def add_guest(self, data: GuestIn) -> Guest | None:
        """The abstract adding new guest to the data storage.

        Args:
            data (GuestIn): The details of the new guest.

        Returns:
            Guest | None: The newly added guest.
        """

    @abstractmethod
    async def update_guest(
            self,
            guest_id: int,
            data: GuestIn,
    ) -> Guest | None:
        """The abstract updating guest data in the data storage.

        Args:
            guest_id (int): The id of the guest.
            data (GuestIn): The details of the updated guest.

        Returns:
            Guest | None: The updated guest details.
        """

    @abstractmethod
    async def delete_guest(self, guest_id: int) -> bool:
        """The abstract updating removing guest from the data storage.

        Args:
            guest_id (int): The id of the guest.

        Returns:
            bool: Success of the operation.
        """