"""
Module for managing accessibility_option service abstractions.
"""

from abc import ABC, abstractmethod
from typing import List

from hotel_management_system.core.domains.accessibility_option import AccessibilityOption, AccessibilityOptionIn


class IAccessibilityOptionService(ABC):
    """
    Abstract base class defining the interface for an accessibility option service.
    """

    @abstractmethod
    async def get_all(self) -> List[AccessibilityOption]:
        """
        Retrieve all accessibility options from the data storage.

        Returns:
            List[AccessibilityOption]: A collection of all accessibility options.
        """

    @abstractmethod
    async def add_accessibility_option(self, data: AccessibilityOptionIn) -> AccessibilityOption | None:
        """
        Add a new accessibility option to the data storage.

        Args:
            data (AccessibilityOptionIn): The data for the new accessibility option.

        Returns:
            AccessibilityOption | None: The newly added accessibility option, or None if the operation fails.
        """

    @abstractmethod
    async def get_by_id(self, accessibility_option_id: int) -> AccessibilityOption | None:
        """
        Retrieve an accessibility option by its ID.

        Args:
            accessibility_option_id (int): The ID of the accessibility option.

        Returns:
            AccessibilityOption | None: The accessibility option details, or None if not found.
        """

    @abstractmethod
    async def get_by_name(self, accessibility_option_name: str) -> AccessibilityOption | None:
        """
        Retrieve an accessibility option by its name.

        Args:
            accessibility_option_name (str): The name of the accessibility option.

        Returns:
            AccessibilityOption | None: The accessibility option details, or None if not found.
        """

    @abstractmethod
    async def update_accessibility_option(
            self,
            accessibility_option_id: int,
            data: AccessibilityOptionIn,
    ) -> AccessibilityOption | None:
        """
        Update an existing accessibility option in the data storage.

        Args:
            accessibility_option_id (int): The ID of the accessibility option to update.
            data (AccessibilityOptionIn): The updated data for the accessibility option.

        Returns:
            AccessibilityOption | None: The updated accessibility option, or None if not found.
        """

    @abstractmethod
    async def delete_accessibility_option(self, accessibility_option_id: int) -> bool:
        """
        Remove an accessibility option from the data storage.

        Args:
            accessibility_option_id (int): The ID of the accessibility option to delete.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """