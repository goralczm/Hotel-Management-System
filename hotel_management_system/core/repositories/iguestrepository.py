"""Module containing guest repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from hotel_management_system.core.domains.guest import GuestIn


class IGuestRepository(ABC):
    """An abstract class representing protocol of continent repository."""

    @abstractmethod
    async def get_all_guests(self) -> Iterable[Any]:
        """The abstract getting all guests from the data storage.

        Returns:
            Iterable[Any]: Guests in the data storage.
        """

    @abstractmethod
    async def add_guest(self, data: GuestIn) -> Any | None:
        """The abstract adding new guest to the data storage.

        Args:
            data (GuestIn): The details of the new guest.

        Returns:
            Any | None: The newly added guest.
        """

    @abstractmethod
    async def update_guest(
            self,
            guest_id: int,
            data: GuestIn,
    ) -> Any | None:
        """The abstract updating guest data in the data storage.

        Args:
            guest_id (int): The id of the guest.
            data (GuestIn): The details of the updated guest.

        Returns:
            Any | None: The updated guest details.
        """

    @abstractmethod
    async def delete_guest(self, guest_id: int) -> bool:
        """The abstract updating removing guest from the data storage.

        Args:
            guest_id (int): The id of the guest.

        Returns:
            bool: Success of the operation.
        """