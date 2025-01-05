"""Module containing continent service implementation."""

from typing import List

from hotel_management_system.core.domains.room import Room, RoomIn
from hotel_management_system.core.repositories.i_accessibility_option_repository import IAccessibilityOptionRepository
from hotel_management_system.core.repositories.i_room_accessibility_option_repository import \
    IRoomAccessibilityOptionRepository
from hotel_management_system.core.repositories.i_room_repository import IRoomRepository
from hotel_management_system.core.services.i_room_service import IRoomService


class RoomService(IRoomService):
    """A class implementing the room service."""

    _room_repository: IRoomRepository
    _room_accessibility_option_repository: IRoomAccessibilityOptionRepository
    _accessibility_option_repository: IAccessibilityOptionRepository

    def __init__(self,
                 room_repository: IRoomRepository,
                 room_accessibility_option_repository: IRoomAccessibilityOptionRepository,
                 accessibility_option_repository: IAccessibilityOptionRepository
                 ) -> None:
        """The initializer of the `room service`.

        Args:
            repository (IroomRepository): The reference to the repository.
        """

        self._room_repository = room_repository
        self._room_accessibility_option_repository = room_accessibility_option_repository
        self._accessibility_option_repository = accessibility_option_repository

    async def get_all(self) -> List[Room]:
        """The method getting all rooms from the repository.

        Returns:
            Iterable[roomDTO]: All rooms.
        """

        all_rooms = await self._room_repository.get_all_rooms()

        return [await self.parse_room(room) for room in all_rooms]

    async def get_all_free_rooms(self) -> List[Room]:
        """The method getting all free rooms from the repository.

        Returns:
            Iterable[roomDTO]: All free rooms.
        """

        free_rooms = await self._room_repository.get_all_free_rooms()

        return [await self.parse_room(room) for room in free_rooms]

    async def get_by_id(self, room_id: int) -> Room | None:
        """The method getting room by provided id.

        Args:
            room_id (int): The id of the room.

        Returns:
            roomDTO | None: The room details.
        """

        return await self.parse_room(
            await self._room_repository.get_by_id(room_id)
        )

    async def add_room(self, data: RoomIn) -> Room | None:
        """The method adding new room to the data storage.

        Args:
            data (roomIn): The details of the new room.

        Returns:
            room | None: Full details of the newly added room.
        """

        return await self.parse_room(
            await self._room_repository.add_room(data)
        )

    async def update_room(
            self,
            room_id: int,
            data: RoomIn,
    ) -> Room | None:
        """The method updating room data in the data storage.

        Args:
            room_id (int): The id of the room.
            data (roomIn): The details of the updated room.

        Returns:
            room | None: The updated room details.
        """

        return await self.parse_room(
            await self._room_repository.update_room(
                room_id=room_id,
                data=data,
            )
        )

    async def delete_room(self, room_id: int) -> bool:
        """The method updating removing room from the data storage.

        Args:
            room_id (int): The id of the room.

        Returns:
            bool: Success of the operation.
        """

        return await self._room_repository.delete_room(room_id)

    async def parse_room(self, room: Room) -> Room:
        if room:
            room_accessibility_options = await self._room_accessibility_option_repository.get_by_room_id(room.id)

            accessibility_options = []

            for room_accessibility_option in room_accessibility_options:
                accessibility_option = await self._accessibility_option_repository.get_by_id(room_accessibility_option.accessibility_option_id)

                accessibility_options.append(accessibility_option)

            room.accessibility_options = accessibility_options

        return room
