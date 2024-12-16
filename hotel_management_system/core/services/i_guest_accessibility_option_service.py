"""Module containing guest_accessibility_option service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from hotel_management_system.core.domains.guest_accessibility_option import GuestAccessibilityOption, GuestAccessibilityOptionIn


class IGuestAccessibilityOptionService(ABC):
    """A class representing guest_accessibility_option repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[GuestAccessibilityOption]:
        """The method getting all guest_accessibility_options from the repository.

        Returns:
            Iterable[guest_accessibility_optionDTO]: All guest_accessibility_options.
        """

    @abstractmethod
    async def get_by_id(self, guest_id: int, accessibility_option_id: int) -> GuestAccessibilityOption | None:
        """The method getting guest_accessibility_option by provided id.

        Args:
            guest_id (int): The id of the guest
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            guest_accessibility_optionDTO | None: The guest_accessibility_option details.
        """

    @abstractmethod
    async def get_by_guest_id(self, guest_id: int) -> Iterable[GuestAccessibilityOption] | None:
        """The method getting guest_accessibility_option by provided guest_id.

        Args:
            guest_id (int): The id of the guest

        Returns:
            ReservationRoom | None: The accessibility_option_guest details.
        """

    @abstractmethod
    async def get_by_accessibility_option_id(self, accessibility_option_id: int) -> Iterable[GuestAccessibilityOption] | None:
        """The method getting guest_accessibility_option's by provided accessibility_option id.

        Args:
            accessibility_option_id (int): The id of the accessibility_option

        Returns:
            ReservationRoom | None: The accessibility_option_guest details.
        """

    @abstractmethod
    async def add_guest_accessibility_option(self, data: GuestAccessibilityOptionIn) -> GuestAccessibilityOption | None:
        """The method adding new guest_accessibility_option to the data storage.

        Args:
            data (guest_accessibility_optionIn): The details of the new guest_accessibility_option.

        Returns:
            guest_accessibility_option | None: Full details of the newly added guest_accessibility_option.
        """

    @abstractmethod
    async def update_guest_accessibility_option(
            self,
            guest_id: int,
            accessibility_option_id: int,
            data: GuestAccessibilityOptionIn,
    ) -> GuestAccessibilityOption | None:
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