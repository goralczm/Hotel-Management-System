"""
Module containing room_accessibility_option service implementation.
"""

from typing import Iterable, List

from hotel_management_system.core.domains.room_accessibility_option import RoomAccessibilityOption, RoomAccessibilityOptionIn
from hotel_management_system.core.repositories.i_room_accessibility_option_repository import IRoomAccessibilityOptionRepository
from hotel_management_system.core.services.i_room_accessibility_option_service import IRoomAccessibilityOptionService


class RoomAccessibilityOptionService(IRoomAccessibilityOptionService):
    """
    A class implementing the room_accessiblity_option service.
    """

    _repository: IRoomAccessibilityOptionRepository

    def __init__(self, repository: IRoomAccessibilityOptionRepository) -> None:
        """
        The initializer of the `room_accessibility_option service`.

        Args:
            repository (IRoomAccessibilityOptionRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[RoomAccessibilityOption]:
        """
        Retrieve all room accessibility options from the data storage.

        Returns:
            List[RoomAccessibilityOption]: A list of all room accessibility options.
        """

        return await self._repository.get_all_room_accessibility_options()

    async def get_by_id(self, room_id: int, accessibility_option_id: int) -> RoomAccessibilityOption | None:
        """
        Retrieve a room accessibility option by its unique room ID and accessibility option ID.

        Args:
            room_id (int): The ID of the room.
            accessibility_option_id (int): The ID of the accessibility option.

        Returns:
            RoomAccessibilityOption | None: The room accessibility option details if found, or None if not found.
        """

        return await self._repository.get_by_id(room_id, accessibility_option_id)

    async def get_by_room_id(self, room_id: int) -> List[RoomAccessibilityOption]:
        """
        Retrieve room accessibility options for a specific room ID.

        Args:
            room_id (int): The ID of the room.

        Returns:
            RoomAccessibilityOption | None: The room accessibility option details if found
        """

        return await self._repository.get_by_room_id(room_id)

    async def add_room_accessibility_option(self, data: RoomAccessibilityOptionIn) -> RoomAccessibilityOption | None:
        """
        Add a new room accessibility option to the data storage.

        Args:
            data (RoomAccessibilityOption): The details of the new room accessibility option.

        Returns:
            RoomAccessibilityOption | None: The newly added room accessibility option, or None if the operation fails.
        """

        return await self._repository.add_room_accessibility_option(data)

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
            data (RoomAccessibilityOption): The updated details for the room accessibility option.

        Returns:
            RoomAccessibilityOption | None: The updated room accessibility option details, or None if not found.
        """

        return await self._repository.update_room_accessibility_option(
            room_id=room_id,
            accessibility_option_id=accessibility_option_id,
            data=data,
        )

    async def delete_room_accessibility_option(self, room_id: int, accessibility_option_id: int) -> bool:
        """
        Remove a room accessibility option from the data storage.

        Args:
            room_id (int): The ID of the room.
            accessibility_option_id (int): The ID of the accessibility option.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """

        return await self._repository.delete_room_accessibility_option(room_id, accessibility_option_id)
