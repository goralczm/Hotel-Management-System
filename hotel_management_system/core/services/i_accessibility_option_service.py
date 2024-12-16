"""Module containing accessibility_option service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from hotel_management_system.core.domains.accessibility_option import AccessibilityOption, AccessibilityOptionIn


class IAccessibilityOptionService(ABC):
    """A class representing accessibility_option repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[AccessibilityOption]:
        """The method getting all accessibility_options from the repository.

        Returns:
            Iterable[accessibility_optionDTO]: All accessibility_options.
        """

    @abstractmethod
    async def get_by_id(self, accessibility_option_id: int) -> AccessibilityOption | None:
        """The method getting accessibility_option by provided id.

        Args:
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            accessibility_optionDTO | None: The accessibility_option details.
        """

    @abstractmethod
    async def get_by_name(self, accessibility_option_name: str) -> AccessibilityOption | None:
        """The method getting accessibility_option by provided name.

        Args:
            accessibility_option_name (str): The name of the accessibility_option.

        Returns:
            accessibility_optionDTO | None: The accessibility_option details.
        """

    @abstractmethod
    async def add_accessibility_option(self, data: AccessibilityOptionIn) -> AccessibilityOption | None:
        """The method adding new accessibility_option to the data storage.

        Args:
            data (accessibility_optionIn): The details of the new accessibility_option.

        Returns:
            accessibility_option | None: Full details of the newly added accessibility_option.
        """

    @abstractmethod
    async def setup_accessibility_options(self) -> None:
        """The method initiating accessibility_option data in the data storage.

        Returns:
            None
        """

    @abstractmethod
    async def update_accessibility_option(
            self,
            accessibility_option_id: int,
            data: AccessibilityOptionIn,
    ) -> AccessibilityOption | None:
        """The method updating accessibility_option data in the data storage.

        Args:
            accessibility_option_id (int): The id of the accessibility_option.
            data (accessibility_optionIn): The details of the updated accessibility_option.

        Returns:
            accessibility_option | None: The updated accessibility_option details.
        """

    @abstractmethod
    async def delete_accessibility_option(self, accessibility_option_id: int) -> bool:
        """The method updating removing accessibility_option from the data storage.

        Args:
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
        """