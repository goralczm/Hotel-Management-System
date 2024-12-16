"""Module containing guest_accessibility_option repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from hotel_management_system.core.domains.guest_accessibility_option import GuestAccessibilityOptionIn

class IGuestAccessibilityOptionRepository(ABC):
    """An abstract class representing protocol of continent repository."""

    @abstractmethod
    async def get_all_guest_accessibility_options(self) -> Iterable[Any]:
        """The abstract getting all guest_accessibility_options from the data storage.

        Returns:
            Iterable[Any]: Guests in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, guest_id: int, accessibility_option_id: int) -> Any | None:
        """The method getting guest_accessibility_option by provided id.

        Args:
            guest_id (int): The id of the guest
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            guest_accessibility_optionDTO | None: The guest_accessibility_option details.
        """

    @abstractmethod
    async def get_by_guest_id(self, guest_id: int) -> Any | None:
        """The method getting guest_accessibility_option by provided guest_id.

        Args:
            guest_id (int): The id of the guest

        Returns:
            ReservationRoom | None: The accessibility_option_guest details.
        """

    @abstractmethod
    async def get_by_accessibility_option_id(self, accessibility_option_id: int) -> Any | None:
        """The method getting guest_accessibility_option's by provided accessibility_option id.

        Args:
            accessibility_option_id (int): The id of the accessibility_option

        Returns:
            ReservationRoom | None: The accessibility_option_guest details.
        """

    @abstractmethod
    async def add_guest_accessibility_option(self, data: GuestAccessibilityOptionIn) -> Any | None:
        """The abstract adding new guest_accessibility_option to the data storage.

        Args:
            data (GuestIn): The details of the new guest_accessibility_option.

        Returns:
            Any | None: The newly added guest_accessibility_option.
        """

    @abstractmethod
    async def update_guest_accessibility_option(
            self,
            guest_id: int,
            accessibility_option_id: int,
            data: GuestAccessibilityOptionIn,
    ) -> Any | None:
        """The abstract updating guest_accessibility_option data in the data storage.

        Args:
            guest_id (int): The id of the guest.
            accessibility_option_id (int): The id of the accessibility_option.
            data (GuestIn): The details of the updated guest_accessibility_option.

        Returns:
            Any | None: The updated guest_accessibility_option details.
        """

    @abstractmethod
    async def delete_guest_accessibility_option(self, guest_id: int, accessibility_option_id: int) -> bool:
        """The abstract updating removing guest_accessibility_option from the data storage.

        Args:
            guest_id (int): The id of the guest
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
        """