"""Module containing guest service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from hotel_management_system.core.domains.guest import Guest, GuestIn


class IGuestService(ABC):
    """A class representing guest repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[Guest]:
        """The method getting all guests from the repository.

        Returns:
            Iterable[guestDTO]: All guests.
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
    async def add_guest(self, data: GuestIn) -> Guest | None:
        """The method adding new guest to the data storage.

        Args:
            data (guestIn): The details of the new guest.

        Returns:
            guest | None: Full details of the newly added guest.
        """

    @abstractmethod
    async def update_guest(
            self,
            guest_id: int,
            data: GuestIn,
    ) -> Guest | None:
        """The method updating guest data in the data storage.

        Args:
            guest_id (int): The id of the guest.
            data (guestIn): The details of the updated guest.

        Returns:
            guest | None: The updated guest details.
        """

    @abstractmethod
    async def delete_guest(self, guest_id: int) -> bool:
        """The method updating removing guest from the data storage.

        Args:
            guest_id (int): The id of the guest.

        Returns:
            bool: Success of the operation.
        """