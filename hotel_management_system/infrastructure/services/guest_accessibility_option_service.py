"""Module containing continent service implementation."""

from typing import Iterable

from hotel_management_system.core.domains.guest_accessibility_option import GuestAccessibilityOption, GuestAccessibilityOptionIn
from hotel_management_system.core.repositories.i_guest_accessibility_option_repository import IGuestAccessibilityOptionRepository
from hotel_management_system.core.services.i_guest_accessibility_option_service import IGuestAccessibilityOptionService


class GuestAccessibilityOptionService(IGuestAccessibilityOptionService):
    """A class implementing the guest_accessibility_option service."""

    _repository: IGuestAccessibilityOptionRepository

    def __init__(self, repository: IGuestAccessibilityOptionRepository) -> None:
        """The initializer of the `guest_accessibility_option service`.

        Args:
            repository (Iguest_accessibility_optionRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[GuestAccessibilityOption]:
        """The method getting all guest_accessibility_options from the repository.

        Returns:
            Iterable[guest_accessibility_optionDTO]: All guest_accessibility_options.
        """

        return await self._repository.get_all_guest_accessibility_options()

    async def get_by_id(self, guest_id: int, accessibility_option_id: int) -> GuestAccessibilityOption | None:
        """The method getting guest_accessibility_option by provided id.

        Args:
            guest_id (int): The id of the guest
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            guest_accessibility_optionDTO | None: The guest_accessibility_option details.
        """

        return await self._repository.get_by_id(guest_id, accessibility_option_id)

    async def get_by_guest_id(self, guest_id: int) -> Iterable[GuestAccessibilityOption] | None:
        """The method getting guest_accessibility_option by provided guest_id.

        Args:
            guest_id (int): The id of the guest

        Returns:
            ReservationRoom | None: The accessibility_option_guest details.
        """

        return await self._repository.get_by_guest_id(guest_id)

    async def get_by_accessibility_option_id(self, accessibility_option_id: int) -> Iterable[GuestAccessibilityOption] | None:
        """The method getting guest_accessibility_option's by provided accessibility_option id.

        Args:
            accessibility_option_id (int): The id of the accessibility_option

        Returns:
            ReservationRoom | None: The accessibility_option_guest details.
        """

        return await self._repository.get_by_accessibility_option_id(accessibility_option_id)

    async def add_guest_accessibility_option(self, data: GuestAccessibilityOptionIn) -> GuestAccessibilityOption | None:
        """The method adding new guest_accessibility_option to the data storage.

        Args:
            data (guest_accessibility_optionIn): The details of the new guest_accessibility_option.

        Returns:
            guest_accessibility_option | None: Full details of the newly added guest_accessibility_option.
        """

        return await self._repository.add_guest_accessibility_option(data)

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

        return await self._repository.update_guest_accessibility_option(
            guest_id=guest_id,
            accessibility_option_id=accessibility_option_id,
            data=data,
        )

    async def delete_guest_accessibility_option(self, guest_id: int, accessibility_option_id: int) -> bool:
        """The abstract updating removing guest_accessibility_option from the data storage.

        Args:
            guest_id (int): The id of the guest
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_guest_accessibility_option(guest_id, accessibility_option_id)
