"""
Module containing reservation_room service implementation.
"""

from typing import Iterable, List

from hotel_management_system.core.domains.reservation_room import ReservationRoom, ReservationRoomIn
from hotel_management_system.core.repositories.i_reservation_room_repository import IReservationRoomRepository
from hotel_management_system.core.services.i_reservation_room_service import IReservationRoomService


class ReservationRoomService(IReservationRoomService):
    """
    A class implementing the reservation_room service.
    """

    _repository: IReservationRoomRepository

    def __init__(self, repository: IReservationRoomRepository) -> None:
        """
        The initializer of the `reservation_room service`.

        Args:
            repository (IReservationRoomRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[ReservationRoom]:
        """
        Retrieve all reservation rooms from the data storage.

        Returns:
            List[ReservationRoom]: A list of all reservation rooms.
        """

        return await self._repository.get_all_reservation_rooms()

    async def get_by_id(self, room_id: int, reservation_id: int) -> List[ReservationRoom] | None:
        """
        Retrieve a reservation room by its unique room ID and reservation ID.

        Args:
            room_id (int): The ID of the room.
            reservation_id (int): The ID of the reservation.

        Returns:
            List[ReservationRoom] | None: The reservation room details if found, or None if not found.
        """

        return await self._repository.get_by_id(room_id, reservation_id)

    async def get_by_reservation_id(self, reservation_id: int) -> List[ReservationRoom]:
        """
        Retrieve a reservation room by its reservation ID.

        Args:
            reservation_id (int): The ID of the reservation.

        Returns:
            ReservationRoom | None: The reservation room details if found
        """

        return await self._repository.get_by_reservation_id(reservation_id)

    async def get_by_room_id(self, room_id: int) -> ReservationRoom | None:
        """
        Retrieve reservation rooms for a specific room ID.

        Args:
            room_id (int): The ID of the room.

        Returns:
            List[ReservationRoom] | None: The reservation rooms for the specified room, or None if no rooms are found.
        """
        return await self._repository.get_by_room_id(room_id)

    async def add_reservation_room(self, data: ReservationRoomIn) -> ReservationRoom | None:
        """
        Add a new reservation room to the data storage.

        Args:
            data (ReservationRoomIn): The details of the new reservation room.

        Returns:
            ReservationRoom | None: The newly added reservation room, or None if the operation fails.
        """

        return await self._repository.add_reservation_room(data)

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

        return await self._repository.update_reservation_room(
            room_id=room_id,
            reservation_id=reservation_id,
            data=data,
        )

    async def delete_reservation_room(self, room_id: int, reservation_id: int) -> bool:
        """
        Remove a reservation room from the data storage.

        Args:
            room_id (int): The ID of the room.
            reservation_id (int): The ID of the reservation.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """

        return await self._repository.delete_reservation_room(room_id, reservation_id)
