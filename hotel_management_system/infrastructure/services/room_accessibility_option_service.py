"""Module containing continent service implementation."""

from typing import Iterable

from hotel_management_system.core.domains.room_accessibility_option import RoomAccessibilityOption, RoomAccessibilityOptionIn
from hotel_management_system.core.repositories.i_room_accessibility_option_repository import IRoomAccessibilityOptionRepository
from hotel_management_system.core.services.i_room_accessibility_option_service import IRoomAccessibilityOptionService


class RoomAccessibilityOptionService(IRoomAccessibilityOptionService):
    """A class implementing the room_accessibility_option service."""

    _repository: IRoomAccessibilityOptionRepository

    def __init__(self, repository: IRoomAccessibilityOptionRepository) -> None:
        """The initializer of the `room_accessibility_option service`.

        Args:
            repository (Iroom_accessibility_optionRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[RoomAccessibilityOption]:
        """The method getting all room_accessibility_options from the repository.

        Returns:
            Iterable[room_accessibility_optionDTO]: All room_accessibility_options.
        """

        return await self._repository.get_all_room_accessibility_options()

    async def get_by_id(self, room_id: int, accessibility_option_id: int) -> RoomAccessibilityOption | None:
        """The method getting room_accessibility_option by provided id.

        Args:
            room_id (int): The id of the room
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            room_accessibility_optionDTO | None: The room_accessibility_option details.
        """

        return await self._repository.get_by_id(room_id, accessibility_option_id)

    async def add_room_accessibility_option(self, data: RoomAccessibilityOptionIn) -> RoomAccessibilityOption | None:
        """The method adding new room_accessibility_option to the data storage.

        Args:
            data (room_accessibility_optionIn): The details of the new room_accessibility_option.

        Returns:
            room_accessibility_option | None: Full details of the newly added room_accessibility_option.
        """

        return await self._repository.add_room_accessibility_option(data)

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

        return await self._repository.update_room_accessibility_option(
            room_id=room_id,
            accessibility_option_id=accessibility_option_id,
            data=data,
        )

    async def delete_room_accessibility_option(self, room_id: int, accessibility_option_id: int) -> bool:
        """The abstract updating removing room_accessibility_option from the data storage.

        Args:
            room_id (int): The id of the room
            accessibility_option_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_room_accessibility_option(room_id, accessibility_option_id)
