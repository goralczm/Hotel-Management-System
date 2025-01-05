"""Module containing continent service implementation."""

from typing import Iterable

from hotel_management_system.core.domains.guest import Guest, GuestIn
from hotel_management_system.core.repositories.i_guest_repository import IGuestRepository
from hotel_management_system.core.services.i_accessibility_option_service import IAccessibilityOptionService
from hotel_management_system.core.services.i_guest_accessibility_option_service import IGuestAccessibilityOptionService
from hotel_management_system.core.services.i_guest_service import IGuestService


class GuestService(IGuestService):
    """A class implementing the guest service."""

    _guest_repository: IGuestRepository
    _accessibility_option_repository: IAccessibilityOptionService
    _guest_accessibility_option_repository: IGuestAccessibilityOptionService

    def __init__(self,
                 guest_repository: IGuestRepository,
                 accessibility_option_repository: IAccessibilityOptionService,
                 guest_accessibility_option_repository: IGuestAccessibilityOptionService,
                 ) -> None:
        """The initializer of the `guest service`.

        Args:
            repository (IguestRepository): The reference to the repository.
        """

        self._guest_repository = guest_repository
        self._accessibility_option_repository = accessibility_option_repository
        self._guest_accessibility_option_repository = guest_accessibility_option_repository

    async def get_all(self) -> Iterable[Guest]:
        """The method getting all guests from the repository.

        Returns:
            Iterable[guestDTO]: All guests.
        """

        all_guests = await self._guest_repository.get_all_guests()

        return [await self.parse_guest(guest) for guest in all_guests]

    async def get_by_id(self, guest_id: int) -> Guest | None:
        """The method getting guest by provided id.

        Args:
            guest_id (int): The id of the guest.

        Returns:
            guestDTO | None: The guest details.
        """

        return await self.parse_guest(
            await self._guest_repository.get_by_id(guest_id)
        )

    async def add_guest(self, data: GuestIn) -> Guest | None:
        """The method adding new guest to the data storage.

        Args:
            data (guestIn): The details of the new guest.

        Returns:
            guest | None: Full details of the newly added guest.
        """

        return await self.parse_guest(
            await self._guest_repository.add_guest(data)
        )

    async def update_guest(
            self,
            guest_id: int,
            data: GuestIn,
    ) -> Guest | None:
        """The method updating guest data in the data storage.

        Args:
            guest_id (int): The id of the guest.
            data (guestIn): The details of the updated guest.

        Returns:
            guest | None: The updated guest details.
        """

        return await self.parse_guest(
            await self._guest_repository.update_guest(
                guest_id=guest_id,
                data=data,
            )
        )

    async def delete_guest(self, guest_id: int) -> bool:
        """The method updating removing guest from the data storage.

        Args:
            guest_id (int): The id of the guest.

        Returns:
            bool: Success of the operation.
        """

        return await self._guest_repository.delete_guest(guest_id)

    async def parse_guest(self, guest: Guest) -> Guest:
        if guest:
            accessibility_options = []

            guest_accessibility_options = await self._guest_accessibility_option_repository.get_by_guest_id(guest.id)

            for guest_accessibility_option in guest_accessibility_options:
                accessibility_option = await self._accessibility_option_repository.get_by_id(guest_accessibility_option.accessibility_option_id)
                accessibility_options.append(accessibility_option)

            guest.accessibility_options = accessibility_options

        return guest
