"""
Module for managing reservation_room service abstractions.
"""

from abc import ABC, abstractmethod
from typing import Iterable, List

from hotel_management_system.core.domains.reservation_room import ReservationRoom, ReservationRoomIn


class IReservationRoomService(ABC):
    """A class representing reservation_room repository."""

    @abstractmethod
    async def get_all(self) -> List[ReservationRoom]:
        """
        Retrieve all reservation rooms from the data storage.

        Returns:
            List[ReservationRoom]: A list of all reservation rooms.
        """

    @abstractmethod
    async def get_by_id(self, room_id: int, reservation_id: int) -> List[ReservationRoom] | None:
        """
        Retrieve a reservation room by its unique room ID and reservation ID.

        Args:
            room_id (int): The ID of the room.
            reservation_id (int): The ID of the reservation.

        Returns:
            List[ReservationRoom] | None: The reservation room details if found, or None if not found.
        """

    @abstractmethod
    async def get_by_room_id(self, room_id: int) -> List[ReservationRoom] | None:
        """
        Retrieve reservation rooms for a specific room ID.

        Args:
            room_id (int): The ID of the room.

        Returns:
            List[ReservationRoom] | None: The reservation rooms for the specified room, or None if no rooms are found.
        """

    @abstractmethod
    async def get_by_reservation_id(self, reservation_id: int) -> List[ReservationRoom]:
        """
        Retrieve a reservation room by its reservation ID.

        Args:
            reservation_id (int): The ID of the reservation.

        Returns:
            ReservationRoom | None: The reservation room details if found
        """

    @abstractmethod
    async def add_reservation_room(self, data: ReservationRoomIn) -> ReservationRoom | None:
        """
        Add a new reservation room to the data storage.

        Args:
            data (ReservationRoomIn): The details of the new reservation room.

        Returns:
            ReservationRoom | None: The newly added reservation room, or None if the operation fails.
        """

    @abstractmethod
    async def update_reservation_room(
            self,
            room_id: int,
            reservation_id: int,
            data: ReservationRoomIn,
    ) -> ReservationRoom | None:
        """
        Update the details of an existing reservation room in the data storage.

        Args:
            room_id (int): The ID of the room.
            reservation_id (int): The ID of the reservation.
            data (ReservationRoomIn): The updated details for the reservation room.

        Returns:
            ReservationRoom | None: The updated reservation room details, or None if the reservation room is not found.
        """

    @abstractmethod
    async def delete_reservation_room(self, room_id: int, reservation_id: int) -> bool:
        """
        Remove a reservation room from the data storage.

        Args:
            room_id (int): The ID of the room.
            reservation_id (int): The ID of the reservation.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
