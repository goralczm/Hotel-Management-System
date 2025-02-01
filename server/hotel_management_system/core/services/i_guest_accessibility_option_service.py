"""
Module for managing guest_accessibility_option service abstractions.
"""

from abc import ABC, abstractmethod
from typing import List

from hotel_management_system.core.domains.guest_accessibility_option import GuestAccessibilityOption, GuestAccessibilityOptionIn


class IGuestAccessibilityOptionService(ABC):
    """A class representing guest_accessibility_option repository."""

    @abstractmethod
    async def get_all(self) -> List[GuestAccessibilityOption]:
        """
        Retrieve all guest accessibility options from the data storage.

        Returns:
            List[GuestAccessibilityOption]: A collection of all guest accessibility options.
        """

    @abstractmethod
    async def get_by_id(self, guest_id: int, accessibility_option_id: int) -> GuestAccessibilityOption | None:
        """
        Retrieve a guest accessibility option by guest ID and accessibility option ID.

        Args:
            guest_id (int): The ID of the guest.
            accessibility_option_id (int): The ID of the accessibility option.

        Returns:
            GuestAccessibilityOption | None: The details of the guest accessibility option if found
        """

    @abstractmethod
    async def get_by_guest_id(self, guest_id: int) -> List[GuestAccessibilityOption] | None:
        """
        Retrieve all accessibility options associated with a specific guest ID.

        Args:
            guest_id (int): The ID of the guest.

        Returns:
            List[GuestAccessibilityOption]: A collection of guest accessibility options if found
        """

    @abstractmethod
    async def get_by_accessibility_option_id(self, accessibility_option_id: int) -> List[GuestAccessibilityOption] | None:
        """
        Retrieve all guest accessibility options associated with a specific accessibility option ID.

        Args:
            accessibility_option_id (int): The ID of the accessibility option.

        Returns:
            List[GuestAccessibilityOption]: A collection of guest accessibility options if found
        """

    @abstractmethod
    async def add_guest_accessibility_option(self, data: GuestAccessibilityOptionIn) -> GuestAccessibilityOption | None:
        """
        Add a new guest accessibility option to the data storage.

        Args:
            data (GuestAccessibilityOptionIn): The details of the new guest accessibility option.

        Returns:
            GuestAccessibilityOption | None: The newly added guest accessibility option, or None if the operation fails.
        """

    @abstractmethod
    async def update_guest_accessibility_option(
            self,
            guest_id: int,
            accessibility_option_id: int,
            data: GuestAccessibilityOptionIn,
    ) -> GuestAccessibilityOption | None:
        """
        Update an existing guest accessibility option in the data storage.

        Args:
            guest_id (int): The ID of the guest.
            accessibility_option_id (int): The ID of the accessibility option.
            data (GuestAccessibilityOptionIn): The updated data for the guest accessibility option.

        Returns:
            GuestAccessibilityOption | None: The updated guest accessibility option, or None if not found.
        """

    @abstractmethod
    async def delete_guest_accessibility_option(self, guest_id: int, accessibility_option_id: int) -> bool:
        """
        Remove a guest accessibility option from the data storage.

        Args:
            guest_id (int): The ID of the guest.
            accessibility_option_id (int): The ID of the accessibility option.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
