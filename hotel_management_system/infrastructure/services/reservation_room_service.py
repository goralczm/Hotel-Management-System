"""Module containing continent service implementation."""

from typing import Iterable, List

from hotel_management_system.core.domains.reservation_room import ReservationRoom, ReservationRoomIn
from hotel_management_system.core.repositories.i_reservation_room_repository import IReservationRoomRepository
from hotel_management_system.core.services.i_reservation_room_service import IReservationRoomService


class ReservationRoomService(IReservationRoomService):
    """A class implementing the reservation_room service."""

    _repository: IReservationRoomRepository

    def __init__(self, repository: IReservationRoomRepository) -> None:
        """The initializer of the `reservation_room service`.

        Args:
            repository (Ireservation_roomRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[ReservationRoom]:
        """The method getting all reservation_rooms from the repository.

        Returns:
            Iterable[reservation_roomDTO]: All reservation_rooms.
        """

        return await self._repository.get_all_reservation_rooms()

    async def get_by_id(self, room_id: int, reservation_id: int) -> List[ReservationRoom] | None:
        """The method getting reservation_room by provided id.

        Args:
            room_id (int): The id of the room
            reservation_id (int): The id of the accessibility_option.

        Returns:
            reservation_roomDTO | None: The reservation_room details.
        """

        return await self._repository.get_by_id(room_id, reservation_id)

    async def get_by_reservation_id(self, reservation_id: int) -> List[ReservationRoom] | None:
        """The method getting reservation_room's by provided reservation id.

        Args:
            reservation_id (int): The id of the reservation

        Returns:
            ReservationRoom | None: The reservation_room details.
        """

        return await self._repository.get_by_reservation_id(reservation_id)

    async def get_by_room_id(self, room_id: int) -> ReservationRoom | None:
        """The method getting reservation_room by provided room_id.

        Args:
            room_id (int): The id of the room

        Returns:
            ReservationRoom | None: The reservation_room details.
        """

        return await self._repository.get_by_room_id(room_id)

    async def add_reservation_room(self, data: ReservationRoomIn) -> ReservationRoom | None:
        """The method adding new reservation_room to the data storage.

        Args:
            data (reservation_roomIn): The details of the new reservation_room.

        Returns:
            reservation_room | None: Full details of the newly added reservation_room.
        """

        return await self._repository.add_reservation_room(data)

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

        return await self._repository.update_reservation_room(
            room_id=room_id,
            reservation_id=reservation_id,
            data=data,
        )

    async def delete_reservation_room(self, room_id: int, reservation_id: int) -> bool:
        """The abstract updating removing reservation_room from the data storage.

        Args:
            room_id (int): The id of the room
            reservation_id (int): The id of the accessibility_option.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_reservation_room(room_id, reservation_id)
