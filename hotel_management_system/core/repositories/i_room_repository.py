"""Module containing room repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable, List

from hotel_management_system.core.domains.room import RoomIn, Room


class IRoomRepository(ABC):
    """An abstract class representing protocol of continent repository."""

    @abstractmethod
    async def get_all_rooms(self) -> List[Room]:
        """The abstract getting all rooms from the data storage.

        Returns:
            Iterable[Any]: Guests in the data storage.
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
        """The abstract adding new room to the data storage.

        Args:
            data (GuestIn): The details of the new room.

        Returns:
            Any | None: The newly added room.
        """

    @abstractmethod
    async def update_room(
            self,
            room_id: int,
            data: RoomIn,
    ) -> Room | None:
        """The abstract updating room data in the data storage.

        Args:
            room_id (int): The id of the room.
            data (GuestIn): The details of the updated room.

        Returns:
            Any | None: The updated room details.
        """

    @abstractmethod
    async def delete_room(self, room_id: int) -> bool:
        """The abstract updating removing room from the data storage.

        Args:
            room_id (int): The id of the room.

        Returns:
            bool: Success of the operation.
        """