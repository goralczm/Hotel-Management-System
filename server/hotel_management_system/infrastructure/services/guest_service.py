"""
Module containing guest service implementation.
"""

from typing import Iterable, List

from hotel_management_system.core.domains.guest import Guest, GuestIn
from hotel_management_system.core.repositories.i_guest_repository import IGuestRepository
from hotel_management_system.core.services.i_accessibility_option_service import IAccessibilityOptionService
from hotel_management_system.core.services.i_guest_accessibility_option_service import IGuestAccessibilityOptionService
from hotel_management_system.core.services.i_guest_service import IGuestService


class GuestService(IGuestService):
    """
    A class implementing the guest service.
    """

    _guest_repository: IGuestRepository
    _accessibility_option_repository: IAccessibilityOptionService
    _guest_accessibility_option_repository: IGuestAccessibilityOptionService

    def __init__(self,
                 guest_repository: IGuestRepository,
                 accessibility_option_repository: IAccessibilityOptionService,
                 guest_accessibility_option_repository: IGuestAccessibilityOptionService,
                 ) -> None:
        """
        The initializer of the `guest service`.

        Args:
            guest_repository (IGuestRepository): The reference to the guest repository
            accessibility_option_repository (IAccessibilityOptionService): The reference to the
                                                                                accessibility_option repository
            guest_accessibility_option_repository (IGuestAccessibilityOptionService): The reference to the
                                                                                guest_accessibility_option repository
        """

        self._guest_repository = guest_repository
        self._accessibility_option_repository = accessibility_option_repository
        self._guest_accessibility_option_repository = guest_accessibility_option_repository

    async def get_all(self) -> List[Guest]:
        """
        Retrieve all guests from the data storage.

        Returns:
            List[Guest]: A list of all guests.
        """

        all_guests = await self._guest_repository.get_all_guests()

        return [await self.parse_guest(guest) for guest in all_guests]

    async def get_by_id(self, guest_id: int) -> Guest | None:
        """
        Retrieve a guest by their unique ID.

        Args:
            guest_id (int): The ID of the guest.

        Returns:
            Guest | None: The details of the guest if found, or None if not found.
        """

        return await self.parse_guest(
            await self._guest_repository.get_by_id(guest_id)
        )

    async def get_by_first_name(self, first_name: str) -> List[Guest] | None:
        """
        Retrieve guests by their first name.

        Args:
            first_name (str): The first name of the guest(s).

        Returns:
            List[Guest] | None: A list of guests matching the first name, or None if no match is found.
        """

        guests = await self._guest_repository.get_by_first_name(first_name)

        return [
            await self.parse_guest(guest) for guest in guests
        ]

    async def get_by_last_name(self, last_name: str) -> List[Guest] | None:
        """
        Retrieve guests by their last name.

        Args:
            last_name (str): The last name of the guest(s).

        Returns:
            List[Guest] | None: A list of guests matching the last name, or None if no match is found.
        """

        guests = await self._guest_repository.get_by_last_name(last_name)

        return [
            await self.parse_guest(guest) for guest in guests
        ]

    async def get_by_needle_in_name(self, needle: str) -> List[Guest] | None:
        """
        Search for guests whose names contain a specific substring.

        Args:
            needle (str): A substring to search for within guest names.

        Returns:
            List[Guest] | None: A list of guests whose names contain the substring, or None if no match is found.
        """

        guests = await self._guest_repository.get_by_needle_in_name(needle)

        return [
            await self.parse_guest(guest) for guest in guests
        ]

    async def add_guest(self, data: GuestIn) -> Guest | None:
        """
        Add a new guest to the data storage.

        Args:
            data (GuestIn): The details of the new guest.

        Returns:
            Guest | None: The newly added guest, or None if the operation fails.
        """

        return await self.parse_guest(
            await self._guest_repository.add_guest(data)
        )

    async def update_guest(
            self,
            guest_id: int,
            data: GuestIn,
    ) -> Guest | None:
        """
        Update an existing guest's data in the data storage.

        Args:
            guest_id (int): The ID of the guest to update.
            data (GuestIn): The updated details for the guest.

        Returns:
            Guest | None: The updated guest details, or None if the guest is not found.
        """

        return await self.parse_guest(
            await self._guest_repository.update_guest(
                guest_id=guest_id,
                data=data,
            )
        )

    async def delete_guest(self, guest_id: int) -> bool:
        """
        Remove a guest from the data storage.

        Args:
            guest_id (int): The ID of the guest to remove.

        Returns:
            bool: True if the operation is successful, False otherwise.
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
