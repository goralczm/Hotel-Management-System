"""Module containing continent service implementation."""

from typing import Iterable

from hotel_management_system.core.domains.accessibility_option import AccessibilityOption, AccessibilityOptionIn
from hotel_management_system.core.repositories.i_accessibility_option_repository import IAccessibilityOptionRepository
from hotel_management_system.core.services.i_accessibility_option_service import IAccessibilityOptionService


class AccessibilityOptionService(IAccessibilityOptionService):
    """A class implementing the accessibility_option service."""

    _repository: IAccessibilityOptionRepository

    def __init__(self, repository: IAccessibilityOptionRepository) -> None:
        """The initializer of the `accessibility_option service`.

        Args:
            repository (IAccessibilityOptionRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[AccessibilityOption]:
        """The method getting all accessibility_options from the repository.

        Returns:
            Iterable[accessibility_optionDTO]: All accessibility_options.
        """

        return await self._repository.get_all_accessibility_options()

    async def get_by_id(self, accessibility_option_id: int) -> AccessibilityOption | None:
        """The method getting accessibility_option by provided id.

        Args:
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            accessibility_optionDTO | None: The accessibility_option details.
        """

        return await self._repository.get_by_id(accessibility_option_id)

    async def get_by_name(self, accessibility_option_name: str) -> AccessibilityOption | None:
        """The method getting accessibility_option by provided name.

        Args:
            accessibility_option_name (str): The name of the accessibility_option.

        Returns:
            accessibility_optionDTO | None: The accessibility_option details.
        """

        return await self._repository.get_by_name(accessibility_option_name)

    async def add_accessibility_option(self, data: AccessibilityOptionIn) -> AccessibilityOption | None:
        """The method adding new accessibility_option to the data storage.

        Args:
            data (accessibility_optionIn): The details of the new accessibility_option.

        Returns:
            accessibility_option | None: Full details of the newly added accessibility_option.
        """

        return await self._repository.add_accessibility_option(data)

    async def setup_accessibility_options(self):
        await self.add_accessibility_option(AccessibilityOptionIn.from_dict({"name": "Bezpierzowy"}))
        await self.add_accessibility_option(AccessibilityOptionIn.from_dict({"name": "Pierwsze Piętro"}))
        await self.add_accessibility_option(AccessibilityOptionIn.from_dict({"name": "Drugie Piętro"}))
        await self.add_accessibility_option(AccessibilityOptionIn.from_dict({"name": "Niepalący"}))

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

        return await self._repository.update_accessibility_option(
            accessibility_option_id=accessibility_option_id,
            data=data,
        )

    async def delete_accessibility_option(self, accessibility_option_id: int) -> bool:
        """The method updating removing accessibility_option from the data storage.

        Args:
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_accessibility_option(accessibility_option_id)
