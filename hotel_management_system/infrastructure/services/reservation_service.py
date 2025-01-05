"""Module containing continent service implementation."""

from typing import List

from hotel_management_system.core.domains.reservation import Reservation, ReservationIn
from hotel_management_system.core.repositories.i_reservation_repository import IReservationRepository
from hotel_management_system.core.repositories.i_reservation_room_repository import IReservationRoomRepository
from hotel_management_system.core.services.i_bill_service import IBillService
from hotel_management_system.core.services.i_reservation_service import IReservationService
from hotel_management_system.core.services.i_room_service import IRoomService


class ReservationService(IReservationService):
    """A class implementing the reservation service."""

    _reservation_repository: IReservationRepository
    _reservation_room_repository: IReservationRoomRepository
    _room_service: IRoomService
    _bill_service: IBillService

    def __init__(self,
                 reservation_repository: IReservationRepository,
                 reservation_room_repository: IReservationRoomRepository,
                 room_service: IRoomService,
                 bill_service: IBillService,
                 ) -> None:
        """The initializer of the `reservation service`.

        Args:
            repository (IReservationRepository): The reference to the repository.
        """

        self._reservation_repository = reservation_repository
        self._reservation_room_repository = reservation_room_repository
        self._room_service = room_service
        self._bill_service = bill_service

    async def get_all(self) -> List[Reservation]:
        """The method getting all reservations from the repository.

        Returns:
            List[reservationDTO]: All reservations.
        """

        all_reservations = await self._reservation_repository.get_all_reservations()

        return [await self.parse_reservation(reservation) for reservation in all_reservations]

    async def get_by_id(self, reservation_id: int) -> Reservation | None:
        """The method getting reservation by provided id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            reservationDTO | None: The reservation details.
        """

        return await self.parse_reservation(
            await self._reservation_repository.get_by_id(reservation_id)
        )

    async def add_reservation(self, data: ReservationIn) -> Reservation | None:
        """The method adding new reservation to the data storage.

        Args:
            data (reservationIn): The details of the new reservation.

        Returns:
            reservation | None: Full details of the newly added reservation.
        """

        return await self.parse_reservation(
            await self._reservation_repository.add_reservation(data)
        )

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

        return await self.parse_reservation(
            await self._reservation_repository.update_reservation(
                reservation_id=reservation_id,
                data=data,
            )
        )

    async def delete_reservation(self, reservation_id: int) -> bool:
        """The method updating removing reservation from the data storage.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            bool: Success of the operation.
        """

        return await self._reservation_repository.delete_reservation(reservation_id)

    async def parse_reservation(self, reservation: Reservation) -> Reservation:
        if reservation:
            reservation_rooms = await self._reservation_room_repository.get_by_reservation_id(reservation.id)
            reserved_rooms = [await self._room_service.get_by_id(reservation_room.room_id) for reservation_room in reservation_rooms]
            reservation.reserved_rooms = reserved_rooms

            bills = await self._bill_service.get_by_reservation_id(reservation.id)
            reservation.bills = bills

        return reservation
