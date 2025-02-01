"""
Module for managing guest repository abstractions.
"""

from abc import ABC, abstractmethod
from typing import List
from hotel_management_system.core.domains.guest import GuestIn, Guest


class IGuestRepository(ABC):
    """
    Abstract base class defining the interface for a guest repository.
    """

    @abstractmethod
    async def get_all_guests(self) -> List[Guest]:
        """
        Retrieve all guests from the data storage.

        Returns:
            List[Guest]: A list of all guests.
        """

    @abstractmethod
    async def get_by_id(self, guest_id: int) -> Guest | None:
        """
        Retrieve a guest by their unique ID.

        Args:
            guest_id (int): The ID of the guest.

        Returns:
            Guest | None: The details of the guest if found, or None if not found.
        """

    @abstractmethod
    async def get_by_first_name(self, first_name: str) -> List[Guest] | None:
        """
        Retrieve guests by their first name.

        Args:
            first_name (str): The first name of the guest(s).

        Returns:
            List[Guest] | None: A list of guests matching the first name, or None if no match is found.
        """

    @abstractmethod
    async def get_by_last_name(self, last_name: str) -> List[Guest] | None:
        """
        Retrieve guests by their last name.

        Args:
            last_name (str): The last name of the guest(s).

        Returns:
            List[Guest] | None: A list of guests matching the last name, or None if no match is found.
        """

    @abstractmethod
    async def get_by_needle_in_name(self, needle: str) -> List[Guest] | None:
        """
        Search for guests whose names contain a specific substring.

        Args:
            needle (str): A substring to search for within guest names.

        Returns:
            List[Guest] | None: A list of guests whose names contain the substring, or None if no match is found.
        """

    @abstractmethod
    async def add_guest(self, data: GuestIn) -> Guest | None:
        """
        Add a new guest to the data storage.

        Args:
            data (GuestIn): The details of the new guest.

        Returns:
            Guest | None: The newly added guest, or None if the operation fails.
        """

    @abstractmethod
    async def update_guest(self, guest_id: int, data: GuestIn) -> Guest | None:
        """
        Update an existing guest's data in the data storage.

        Args:
            guest_id (int): The ID of the guest to update.
            data (GuestIn): The updated details for the guest.

        Returns:
            Guest | None: The updated guest details, or None if the guest is not found.
        """

    @abstractmethod
    async def delete_guest(self, guest_id: int) -> bool:
        """
        Remove a guest from the data storage.

        Args:
            guest_id (int): The ID of the guest to remove.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
