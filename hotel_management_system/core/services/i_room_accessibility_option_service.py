"""Module containing room_accessibility_option service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from hotel_management_system.core.domains.room_accessibility_option import RoomAccessibilityOption, RoomAccessibilityOptionIn


class IRoomAccessibilityOptionService(ABC):
    """A class representing room_accessibility_option repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[RoomAccessibilityOption]:
        """The method getting all room_accessibility_options from the repository.

        Returns:
            Iterable[room_accessibility_optionDTO]: All room_accessibility_options.
        """

    @abstractmethod
    async def get_by_id(self, room_id: int, accessibility_option_id: int) -> RoomAccessibilityOption | None:
        """The method getting room_accessibility_option by provided id.

        Args:
            room_id (int): The id of the room
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            room_accessibility_optionDTO | None: The room_accessibility_option details.
        """

    @abstractmethod
    async def add_room_accessibility_option(self, data: RoomAccessibilityOptionIn) -> RoomAccessibilityOption | None:
        """The method adding new room_accessibility_option to the data storage.

        Args:
            data (room_accessibility_optionIn): The details of the new room_accessibility_option.

        Returns:
            room_accessibility_option | None: Full details of the newly added room_accessibility_option.
        """

    @abstractmethod
    async def update_room_accessibility_option(
            self,
            room_id: int,
            accessibility_option_id: int,
            data: RoomAccessibilityOptionIn,
    ) -> RoomAccessibilityOption | None:
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