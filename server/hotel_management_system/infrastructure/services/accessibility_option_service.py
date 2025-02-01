"""
Module containing accessibility_option service implementation.
"""

from typing import List

from hotel_management_system.core.domains.accessibility_option import AccessibilityOption, AccessibilityOptionIn
from hotel_management_system.core.repositories.i_accessibility_option_repository import IAccessibilityOptionRepository
from hotel_management_system.core.services.i_accessibility_option_service import IAccessibilityOptionService


class AccessibilityOptionService(IAccessibilityOptionService):
    """
    A class implementing the accessibility_option service.
    """

    _repository: IAccessibilityOptionRepository

    def __init__(self, repository: IAccessibilityOptionRepository) -> None:
        """
        The initializer of the `accessibility_option service`.

        Args:
            repository (IAccessibilityOptionRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> List[AccessibilityOption]:
        """
        Retrieve all accessibility options from the data storage.

        Returns:
            List[AccessibilityOption]: A collection of all accessibility options.
        """

        return await self._repository.get_all_accessibility_options()

    async def add_accessibility_option(self, data: AccessibilityOptionIn) -> AccessibilityOption | None:
        """
        Add a new accessibility option to the data storage.

        Args:
            data (AccessibilityOptionIn): The data for the new accessibility option.

        Returns:
            AccessibilityOption | None: The newly added accessibility option, or None if the operation fails.
        """

        return await self._repository.add_accessibility_option(data)

    async def get_by_id(self, accessibility_option_id: int) -> AccessibilityOption | None:
        """
        Retrieve an accessibility option by its ID.

        Args:
            accessibility_option_id (int): The ID of the accessibility option.

        Returns:
            AccessibilityOption | None: The accessibility option details, or None if not found.
        """

        return await self._repository.get_by_id(accessibility_option_id)

    async def get_by_name(self, accessibility_option_name: str) -> AccessibilityOption | None:
        """
        Retrieve an accessibility option by its name.

        Args:
            accessibility_option_name (str): The name of the accessibility option.

        Returns:
            AccessibilityOption | None: The accessibility option details, or None if not found.
        """

        return await self._repository.get_by_name(accessibility_option_name)

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

        return await self._repository.update_accessibility_option(
            accessibility_option_id=accessibility_option_id,
            data=data,
        )

    async def delete_accessibility_option(self, accessibility_option_id: int) -> bool:
        """
        Remove an accessibility option from the data storage.

        Args:
            accessibility_option_id (int): The ID of the accessibility option to delete.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        return await self._repository.delete_accessibility_option(accessibility_option_id)
