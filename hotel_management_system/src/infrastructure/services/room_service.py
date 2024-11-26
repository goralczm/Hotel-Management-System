"""Module containing continent service implementation."""

from typing import Iterable

from hotel_management_system.src.core.domains.room import Room, RoomIn
from hotel_management_system.src.core.repositories.i_room_repository import IRoomRepository
from hotel_management_system.src.core.services.i_room_service import IRoomService


class RoomService(IRoomService):
    """A class implementing the room service."""

    _repository: IRoomRepository

    def __init__(self, repository: IRoomRepository) -> None:
        """The initializer of the `room service`.

        Args:
            repository (IroomRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[Room]:
        """The method getting all rooms from the repository.

        Returns:
            Iterable[roomDTO]: All rooms.
        """

        return await self._repository.get_all_rooms()

    async def get_by_id(self, room_id: int) -> Room | None:
        """The method getting room by provided id.

        Args:
            room_id (int): The id of the room.

        Returns:
            roomDTO | None: The room details.
        """

        return await self._repository.get_by_id(room_id)

    async def add_room(self, data: RoomIn) -> Room | None:
        """The method adding new room to the data storage.

        Args:
            data (roomIn): The details of the new room.

        Returns:
            room | None: Full details of the newly added room.
        """

        return await self._repository.add_room(data)

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

        return await self._repository.update_room(
            room_id=room_id,
            data=data,
        )

    async def delete_room(self, room_id: int) -> bool:
        """The method updating removing room from the data storage.

        Args:
            room_id (int): The id of the room.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_room(room_id)
