"""Module containing continent service implementation."""

from typing import Iterable

from hotel_management_system.core.domains.reservation import Reservation, ReservationIn
from hotel_management_system.core.repositories.i_reservation_repository import IReservationRepository
from hotel_management_system.core.repositories.i_reservation_room_repository import IReservationRoomRepository
from hotel_management_system.core.repositories.i_room_repository import IRoomRepository
from hotel_management_system.core.services.i_reservation_service import IReservationService


class ReservationService(IReservationService):
    """A class implementing the reservation service."""

    _reservation_repository: IReservationRepository
    _room_repository: IRoomRepository
    _reservation_room_repository: IReservationRoomRepository

    def __init__(self,
                 reservation_repository: IReservationRepository,
                 room_repository: IRoomRepository,
                 reservation_room_repository: IReservationRoomRepository,
                 ) -> None:
        """The initializer of the `reservation service`.

        Args:
            repository (IReservationRepository): The reference to the repository.
        """

        self._reservation_repository = reservation_repository
        self._room_repository = room_repository
        self._reservation_room_repository = reservation_room_repository

    async def get_all(self) -> Iterable[Reservation]:
        """The method getting all reservations from the repository.

        Returns:
            Iterable[reservationDTO]: All reservations.
        """

        return await self._reservation_repository.get_all_reservations()

    async def get_by_id(self, reservation_id: int) -> Reservation | None:
        """The method getting reservation by provided id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            reservationDTO | None: The reservation details.
        """
        reservation = await self._reservation_repository.get_by_id(reservation_id)

        if reservation:
            reservation_rooms = await self._reservation_room_repository.get_by_reservation_id(reservation_id)
            reserved_rooms = [await self._room_repository.get_by_id(reservation_room.room_id) for reservation_room in reservation_rooms]
            reservation.reserved_rooms = reserved_rooms

        return reservation

    async def add_reservation(self, data: ReservationIn) -> Reservation | None:
        """The method adding new reservation to the data storage.

        Args:
            data (reservationIn): The details of the new reservation.

        Returns:
            reservation | None: Full details of the newly added reservation.
        """

        return await self._reservation_repository.add_reservation(data)

    async def update_reservation(
            self,
            reservation_id: int,
            data: ReservationIn,
    ) -> Reservation | None:
        """The method updating reservation data in the data storage.

        Args:
            reservation_id (int): The id of the reservation.
            data (reservationIn): The details of the updated reservation.

        Returns:
            reservation | None: The updated reservation details.
        """

        return await self._reservation_repository.update_reservation(
            reservation_id=reservation_id,
            data=data,
        )

    async def delete_reservation(self, reservation_id: int) -> bool:
        """The method updating removing reservation from the data storage.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            bool: Success of the operation.
        """

        return await self._reservation_repository.delete_reservation(reservation_id)
