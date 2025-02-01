"""
Module for managing room service abstractions.
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import Iterable, List

from hotel_management_system.core.domains.room import Room, RoomIn


class IRoomService(ABC):
    """A class representing room repository."""

    @abstractmethod
    async def get_all(self) -> List[Room]:
        """
        Retrieve all rooms from the data storage.

        Returns:
            List[Room]: A list of all rooms stored in the database.
        """

    @abstractmethod
    async def get_by_id(self, room_id: int) -> Room | None:
        """
        Retrieve a room by its unique ID.

        Args:
            room_id (int): The ID of the room.

        Returns:
            Room | None: The room details if found, or None if no room with the given ID exists.
        """

    @abstractmethod
    async def add_room(self, data: RoomIn) -> Room | None:
        """
        Add a new room to the data storage.

        Args:
            data (RoomIn): The details of the new room.

        Returns:
            Room | None: The newly added room if successful, or None if the operation fails.
        """

    @abstractmethod
    async def update_room(
            self,
            room_id: int,
            data: RoomIn,
    ) -> Room | None:
        """
        Update the details of an existing room in the data storage.

        Args:
            room_id (int): The ID of the room to update.
            data (RoomIn): The updated room details.

        Returns:
            Room | None: The updated room details if successful, or None if no room with the given ID exists.
        """

    @abstractmethod
    async def delete_room(self, room_id: int) -> bool:
        """
        Remove a room from the data storage.

        Args:
            room_id (int): The ID of the room to remove.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
