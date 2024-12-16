"""Module containing accessibility_option repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from hotel_management_system.core.domains.accessibility_option import AccessibilityOptionIn, AccessibilityOption


class IAccessibilityOptionRepository(ABC):
    """An abstract class representing protocol of continent repository."""

    @abstractmethod
    async def get_all_accessibility_options(self) -> Iterable[Any]:
        """The abstract getting all accessibility_options from the data storage.

        Returns:
            Iterable[Any]: Guests in the data storage.
        """

    @abstractmethod
    async def add_accessibility_option(self, data: AccessibilityOptionIn) -> AccessibilityOption | None:
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
    ) -> AccessibilityOption | None:
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

    @abstractmethod
    async def get_by_id(self, accessibility_option_id: int) -> AccessibilityOption | None:
        """The method getting accessibility_option by provided id.

        Args:
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            Any | None: The accessibility_option details.
        """

    @abstractmethod
    async def get_by_name(self, accessibility_option_name: str) -> AccessibilityOption | None:
        """The method getting accessibility_option by provided name.

        Args:
            accessibility_option_name (str): The name of the accessibility_option.

        Returns:
            accessibility_optionDTO | None: The accessibility_option details.
        """