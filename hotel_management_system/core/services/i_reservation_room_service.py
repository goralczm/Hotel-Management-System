"""Module containing reservation_room service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable, List

from hotel_management_system.core.domains.reservation_room import ReservationRoom, ReservationRoomIn


class IReservationRoomService(ABC):
    """A class representing reservation_room repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[ReservationRoom]:
        """The method getting all reservation_rooms from the repository.

        Returns:
            Iterable[reservation_roomDTO]: All reservation_rooms.
        """

    @abstractmethod
    async def get_by_id(self, room_id: int, reservation_id: int) -> ReservationRoom | None:
        """The method getting reservation_room by provided id.

        Args:
            room_id (int): The id of the room
            reservation_id (int): The id of the accessibility_option.

        Returns:
            reservation_roomDTO | None: The reservation_room details.
        """

    @abstractmethod
    async def get_by_room_id(self, room_id: int) -> List[ReservationRoom] | None:
        """The method getting reservation_room by provided room_id.

        Args:
            room_id (int): The id of the room

        Returns:
            ReservationRoom | None: The reservation_room details.
        """

    @abstractmethod
    async def get_by_reservation_id(self, reservation_id: int) -> List[ReservationRoom] | None:
        """The method getting reservation_room's by provided reservation id.

        Args:
            reservation_id (int): The id of the reservation

        Returns:
            ReservationRoom | None: The reservation_room details.
        """

    @abstractmethod
    async def add_reservation_room(self, data: ReservationRoomIn) -> ReservationRoom | None:
        """The method adding new reservation_room to the data storage.

        Args:
            data (reservation_roomIn): The details of the new reservation_room.

        Returns:
            reservation_room | None: Full details of the newly added reservation_room.
        """

    @abstractmethod
    async def update_reservation_room(
            self,
            room_id: int,
            reservation_id: int,
            data: ReservationRoomIn,
    ) -> ReservationRoom | None:
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