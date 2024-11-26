"""Module containing accessibility_option repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from hotel_management_system.src.core.domains.accessibility_option import AccessibilityOptionIn


class IAccessibilityOptionRepository(ABC):
    """An abstract class representing protocol of continent repository."""

    @abstractmethod
    async def get_all_accessibility_options(self) -> Iterable[Any]:
        """The abstract getting all accessibility_options from the data storage.

        Returns:
            Iterable[Any]: Guests in the data storage.
        """

    @abstractmethod
    async def add_accessibility_option(self, data: AccessibilityOptionIn) -> Any | None:
        """The abstract adding new accessibility_option to the data storage.

        Args:
            data (GuestIn): The details of the new accessibility_option.

        Returns:
            Any | None: The newly added accessibility_option.
        """

    @abstractmethod
    async def update_accessibility_option(
            self,
            accessibility_option_id: int,
            data: AccessibilityOptionIn,
    ) -> Any | None:
        """The abstract updating accessibility_option data in the data storage.

        Args:
            accessibility_option_id (int): The id of the accessibility_option.
            data (GuestIn): The details of the updated accessibility_option.

        Returns:
            Any | None: The updated accessibility_option details.
        """

    @abstractmethod
    async def delete_accessibility_option(self, accessibility_option_id: int) -> bool:
        """The abstract updating removing accessibility_option from the data storage.

        Args:
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
        """