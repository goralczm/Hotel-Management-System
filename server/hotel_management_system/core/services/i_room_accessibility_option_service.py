"""
Module for managing room_accessibility_option service abstractions.
"""

from abc import ABC, abstractmethod
from typing import List

from hotel_management_system.core.domains.room_accessibility_option import RoomAccessibilityOption, RoomAccessibilityOptionIn


class IRoomAccessibilityOptionService(ABC):
    """A class representing room_accessibility_option repository."""

    @abstractmethod
    async def get_all(self) -> List[RoomAccessibilityOption]:
        """
        Retrieve all room accessibility options from the data storage.

        Returns:
            List[RoomAccessibilityOption]: A list of all room accessibility options.
        """

    @abstractmethod
    async def get_by_id(self, room_id: int, accessibility_option_id: int) -> RoomAccessibilityOption | None:
        """
        Retrieve a room accessibility option by its unique room ID and accessibility option ID.

        Args:
            room_id (int): The ID of the room.
            accessibility_option_id (int): The ID of the accessibility option.

        Returns:
            RoomAccessibilityOption | None: The room accessibility option details if found, or None if not found.
        """

    @abstractmethod
    async def get_by_room_id(self, room_id: int) -> List[RoomAccessibilityOption]:
        """
        Retrieve room accessibility options for a specific room ID.

        Args:
            room_id (int): The ID of the room.

        Returns:
            RoomAccessibilityOption | None: The room accessibility option details if found
        """

    @abstractmethod
    async def add_room_accessibility_option(self, data: RoomAccessibilityOptionIn) -> RoomAccessibilityOption | None:
        """
        Add a new room accessibility option to the data storage.

        Args:
            data (RoomAccessibilityOptionIn): The details of the new room accessibility option.

        Returns:
            RoomAccessibilityOption | None: The newly added room accessibility option, or None if the operation fails.
        """

    @abstractmethod
    async def update_room_accessibility_option(
            self,
            room_id: int,
            accessibility_option_id: int,
            data: RoomAccessibilityOptionIn,
    ) -> RoomAccessibilityOption | None:
        """
        Update the details of an existing room accessibility option in the data storage.

        Args:
            room_id (int): The ID of the room.
            accessibility_option_id (int): The ID of the accessibility option.
            data (RoomAccessibilityOptionIn): The updated details for the room accessibility option.

        Returns:
            RoomAccessibilityOption | None: The updated room accessibility option details, or None if not found.
        """

    @abstractmethod
    async def delete_room_accessibility_option(self, room_id: int, accessibility_option_id: int) -> bool:
        """
        Remove a room accessibility option from the data storage.

        Args:
            room_id (int): The ID of the room.
            accessibility_option_id (int): The ID of the accessibility option.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
