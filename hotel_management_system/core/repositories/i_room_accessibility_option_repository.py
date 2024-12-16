"""Module containing room_accessibility_option repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from hotel_management_system.core.domains.room_accessibility_option import RoomAccessibilityOptionIn

class IRoomAccessibilityOptionRepository(ABC):
    """An abstract class representing protocol of continent repository."""

    @abstractmethod
    async def get_all_room_accessibility_options(self) -> Iterable[Any]:
        """The abstract getting all room_accessibility_options from the data storage.

        Returns:
            Iterable[Any]: Guests in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, room_id: int, accessibility_option_id: int) -> Any | None:
        """The method getting room_accessibility_option by provided id.

        Args:
            room_id (int): The id of the room
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            room_accessibility_optionDTO | None: The room_accessibility_option details.
        """

    @abstractmethod
    async def add_room_accessibility_option(self, data: RoomAccessibilityOptionIn) -> Any | None:
        """The abstract adding new room_accessibility_option to the data storage.

        Args:
            data (GuestIn): The details of the new room_accessibility_option.

        Returns:
            Any | None: The newly added room_accessibility_option.
        """

    @abstractmethod
    async def update_room_accessibility_option(
            self,
            room_id: int,
            accessibility_option_id: int,
            data: RoomAccessibilityOptionIn,
    ) -> Any | None:
        """The abstract updating room_accessibility_option data in the data storage.

        Args:
            room_id (int): The id of the room.
            accessibility_option_id (int): The id of the accessibility_option.
            data (GuestIn): The details of the updated room_accessibility_option.

        Returns:
            Any | None: The updated room_accessibility_option details.
        """

    @abstractmethod
    async def delete_room_accessibility_option(self, room_id: int, accessibility_option_id: int) -> bool:
        """The abstract updating removing room_accessibility_option from the data storage.

        Args:
            room_id (int): The id of the room
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
        """