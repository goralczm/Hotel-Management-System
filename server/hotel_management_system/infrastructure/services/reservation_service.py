"""
Module containing reservation service implementation.
"""

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
    """
    A class implementing the reservation service.
    """

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
        """
        The initializer of the `reservation service`.

        Args:
            reservation_repository (IReservationRepository): The reference to the reservation repository
            reservation_room_service (IReservationRoomService): The reference to the reservation_room service
            guest_service (IGuestService): The reference to the guest service
            room_service (IRoomService): The reference to the room service
            bill_service (IBillService): The reference to the bill service
        """

        self._reservation_repository = reservation_repository
        self._reservation_room_service = reservation_room_service
        self._guest_service = guest_service
        self._room_service = room_service
        self._bill_service = bill_service

    async def get_all(self) -> List[Reservation]:
        """
        Retrieve all reservations from the data storage.

        Returns:
            List[Reservation]: A list of all reservations.
        """

        all_reservations = await self._reservation_repository.get_all_reservations()

        return [await self.parse_reservation(reservation) for reservation in all_reservations]

    async def get_by_id(self, reservation_id: int) -> Reservation | None:
        """
        Retrieve a reservation by its unique ID.

        Args:
            reservation_id (int): The ID of the reservation.

        Returns:
            Reservation | None: The details of the reservation if found, or None if not found.
        """

        return await self.parse_reservation(
            await self._reservation_repository.get_by_id(reservation_id)
        )

    async def get_by_guest_id(self, guest_id: int) -> List[Reservation] | None:
        """
        Retrieve a list of reservations by the guest ID.

        Args:
            guest_id (int): The ID of the guest.

        Returns:
            List[Reservation]: A list of all reservations with the guest_id.
        """
        all_reservations = await self._reservation_repository.get_all_reservations()
        all_reservations = [reservation for reservation in all_reservations if reservation.guest_id == guest_id]

        return [await self.parse_reservation(reservation) for reservation in all_reservations]

    async def get_by_month(self, year: int, month_number: int) -> List[Reservation]:
        """
        Retrieve reservations made during the specified month.

        Args:
            year (int): The year of the reservations.
            month_number (int): The month number (1 for January, 12 for December).

        Returns:
            List[Reservation]: A list of reservations made in the specified month.
        """

        return [await self.parse_reservation(reservation) for reservation in await self._reservation_repository.get_by_month(year, month_number)]

    async def get_between_dates(self, start_date: date, end_date: date) -> List[Reservation]:
        """
        Retrieve reservations made between the provided start and end dates.

        Args:
            start_date (date): The start date of the range.
            end_date (date): The end date of the range.

        Returns:
            List[Reservation]: A list of reservations made within the date range.
        """

        return [await self.parse_reservation(reservation) for reservation in await self._reservation_repository.get_between_dates(start_date, end_date)]

    async def get_by_year(self, year: int) -> List[Reservation]:
        """
        Retrieve reservations made during the specified year.

        Args:
            year (int): The year of the reservations.

        Returns:
            ist[Reservation]: A list of reservations made in the specified year.
        """

        year_start = datetime.strptime(f'{year}-01-01', '%Y-%m-%d').date()
        year_end = datetime.strptime(f'{year}-12-31', '%Y-%m-%d').date()

        return await self.get_between_dates(year_start, year_end)

    async def get_free_rooms(self, start_date: date, end_date: date) -> List[Room]:
        """
        Retrieve rooms that are not reserved within the provided start and end dates.

        Args:
            start_date (date): The start date of the range.
            end_date (date): The end date of the range.

        Returns:
            List[Room]: A list of free rooms within the date range.
        """

        all_rooms = await self._room_service.get_all()

        reservations = await self.get_between_dates(start_date, end_date)

        reserved_room_ids = set()

        for reservation in reservations:
            reserved_room_ids.update([reserved_room.id for reserved_room in reservation.reserved_rooms])

        free_rooms = [room for room in all_rooms if room.id not in reserved_room_ids]

        return free_rooms

    async def add_reservation(self, data: ReservationIn) -> Reservation | None:
        """
        Add a new reservation to the data storage.

        Args:
            data (ReservationIn): The details of the new reservation.

        Returns:
            Reservation | None: The newly added reservation, or None if the operation fails.
        """

        return await self.parse_reservation(
            await self._reservation_repository.add_reservation(data)
        )

    async def update_reservation(
            self,
            reservation_id: int,
            data: ReservationIn,
    ) -> Reservation | None:
        """
        Update the details of an existing reservation in the data storage.

        Args:
            reservation_id (int): The ID of the reservation to update.
            data (ReservationIn): The updated details for the reservation.

        Returns:
            Reservation | None: The updated reservation details, or None if the reservation is not found.
        """

        return await self.parse_reservation(
            await self._reservation_repository.update_reservation(
                reservation_id=reservation_id,
                data=data,
            )
        )

    async def delete_reservation(self, reservation_id: int) -> bool:
        """
        Remove a reservation from the data storage.

        Args:
            reservation_id (int): The ID of the reservation to remove.

        Returns:
            bool: True if the operation is successful, False otherwise.
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
