"""Module containing continent service implementation."""
from datetime import date, datetime
from typing import List

from hotel_management_system.core.domains.reservation import Reservation, ReservationIn
from hotel_management_system.core.domains.room import Room
from hotel_management_system.core.repositories.i_reservation_repository import IReservationRepository
from hotel_management_system.core.services.i_bill_service import IBillService
from hotel_management_system.core.services.i_guest_service import IGuestService
from hotel_management_system.core.services.i_reservation_room_service import IReservationRoomService
from hotel_management_system.core.services.i_reservation_service import IReservationService
from hotel_management_system.core.services.i_room_service import IRoomService


class ReservationService(IReservationService):
    """A class implementing the reservation service."""

    _reservation_repository: IReservationRepository
    _reservation_room_service: IReservationRoomService
    _guest_service: IGuestService
    _room_service: IRoomService
    _bill_service: IBillService

    def __init__(self,
                 reservation_repository: IReservationRepository,
                 reservation_room_service: IReservationRoomService,
                 guest_service: IGuestService,
                 room_service: IRoomService,
                 bill_service: IBillService,
                 ) -> None:
        """The initializer of the `reservation service`.

        Args:
            repository (IReservationRepository): The reference to the repository.
        """

        self._reservation_repository = reservation_repository
        self._reservation_room_service = reservation_room_service
        self._guest_service = guest_service
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

    async def get_by_month(self, year: int, month_number: int) -> List[Reservation]:
        """The method getting reservations made in the provided month

        Args:
            month_number (int): The month number

        Returns:
            List[Reservation]: The reservations made in provided month
        """

        return [await self.parse_reservation(reservation) for reservation in await self._reservation_repository.get_by_month(year, month_number)]

    async def get_between_dates(self, start_date: date, end_date: date) -> List[Reservation]:
        """The method getting reservations made between provided start_date and end_date

        Args:
            start_date (date): The start date
            end_date (date): The end date

        Returns:
            List[Reservation]: The reservations made between the dates
        """

        return [await self.parse_reservation(reservation) for reservation in await self._reservation_repository.get_between_dates(start_date, end_date)]

    async def get_by_year(self, year: int) -> List[Reservation]:
        year_start = datetime.strptime(f'{year}-01-01', '%Y-%m-%d').date()
        year_end = datetime.strptime(f'{year}-12-31', '%Y-%m-%d').date()

        return await self.get_between_dates(year_start, year_end)

    async def get_free_rooms(self, start_date: date, end_date: date) -> List[Room]:
        """

        :return:
        """

        all_rooms = await self._room_service.get_all()

        free_rooms = []
        for room in all_rooms:
            can_be_reserved = True

            reserved_rooms = await self._reservation_room_service.get_by_room_id(room.id)
            for reserved_room in reserved_rooms:
                reservation = await self.get_by_id(reserved_room.reservation_id)
                if reservation.start_date <= start_date < reservation.end_date and \
                   reservation.start_date < end_date <= reservation.end_date:
                    can_be_reserved = False
                    break

            if can_be_reserved:
                free_rooms.append(room)

        return free_rooms

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
            guest = await self._guest_service.get_by_id(reservation.guest_id)
            reservation.guest = guest

            reservation_rooms = await self._reservation_room_service.get_by_reservation_id(reservation.id)
            reserved_rooms = [await self._room_service.get_by_id(reservation_room.room_id) for reservation_room in reservation_rooms]
            reservation.reserved_rooms = reserved_rooms

            bills = await self._bill_service.get_by_reservation_id(reservation.id)
            reservation.bills = bills

        return reservation
