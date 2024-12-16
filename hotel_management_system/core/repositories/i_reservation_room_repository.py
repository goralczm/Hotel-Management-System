"""Module containing reservation_room repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from hotel_management_system.core.domains.reservation_room import ReservationRoomIn

class IReservationRoomRepository(ABC):
    """An abstract class representing protocol of continent repository."""

    @abstractmethod
    async def get_all_reservation_rooms(self) -> Iterable[Any]:
        """The abstract getting all reservation_rooms from the data storage.

        Returns:
            Iterable[Any]: Guests in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, room_id: int, reservation_id: int) -> Any | None:
        """The method getting reservation_room by provided id.

        Args:
            room_id (int): The id of the room
            reservation_id (int): The id of the accessibility_option.

        Returns:
            reservation_roomDTO | None: The reservation_room details.
        """

    @abstractmethod
    async def get_by_room_id(self, room_id: int) -> Any | None:
        """The method getting reservation_room by provided room_id.

        Args:
            room_id (int): The id of the room

        Returns:
            ReservationRoom | None: The reservation_room details.
        """

    @abstractmethod
    async def get_by_reservation_id(self, reservation_id: int) -> Any | None:
        """The method getting reservation_room's by provided reservation id.

        Args:
            reservation_id (int): The id of the reservation

        Returns:
            ReservationRoom | None: The reservation_room details.
        """

    @abstractmethod
    async def add_reservation_room(self, data: ReservationRoomIn) -> Any | None:
        """The abstract adding new reservation_room to the data storage.

        Args:
            data (GuestIn): The details of the new reservation_room.

        Returns:
            Any | None: The newly added reservation_room.
        """

    @abstractmethod
    async def update_reservation_room(
            self,
            room_id: int,
            reservation_id: int,
            data: ReservationRoomIn,
    ) -> Any | None:
        """The abstract updating reservation_room data in the data storage.

        Args:
            room_id (int): The id of the room.
            reservation_id (int): The id of the accessibility_option.
            data (GuestIn): The details of the updated reservation_room.

        Returns:
            Any | None: The updated reservation_room details.
        """

    @abstractmethod
    async def delete_reservation_room(self, room_id: int, reservation_id: int) -> bool:
        """The abstract updating removing reservation_room from the data storage.

        Args:
            room_id (int): The id of the room
            reservation_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
        """