"""Module containing room service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable, List

from hotel_management_system.core.domains.room import Room, RoomIn


class IRoomService(ABC):
    """A class representing room repository."""

    @abstractmethod
    async def get_all(self) -> List[Room]:
        """The method getting all rooms from the repository.

        Returns:
            Iterable[roomDTO]: All rooms.
        """

    @abstractmethod
    async def get_all_free_rooms(self) -> List[Room]:
        """

        :return:
        """

    @abstractmethod
    async def get_by_id(self, room_id: int) -> Room | None:
        """The method getting room by provided id.

        Args:
            room_id (int): The id of the room.

        Returns:
            roomDTO | None: The room details.
        """

    @abstractmethod
    async def add_room(self, data: RoomIn) -> Room | None:
        """The method adding new room to the data storage.

        Args:
            data (roomIn): The details of the new room.

        Returns:
            room | None: Full details of the newly added room.
        """

    @abstractmethod
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

    @abstractmethod
    async def delete_room(self, room_id: int) -> bool:
        """The method updating removing room from the data storage.

        Args:
            room_id (int): The id of the room.

        Returns:
            bool: Success of the operation.
        """