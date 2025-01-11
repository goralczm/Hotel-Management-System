"""Module containing reservation service abstractions."""

from abc import ABC, abstractmethod
from datetime import date
from typing import Iterable, List

from hotel_management_system.core.domains.reservation import Reservation, ReservationIn
from hotel_management_system.core.domains.room import Room


class IReservationService(ABC):
    """A class representing reservation repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[Reservation]:
        """The method getting all reservations from the repository.

        Returns:
            Iterable[reservationDTO]: All reservations.
        """

    @abstractmethod
    async def get_by_id(self, reservation_id: int) -> Reservation | None:
        """The method getting reservation by provided id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            reservationDTO | None: The reservation details.
        """

    @abstractmethod
    async def get_free_rooms(self, start_date: date, end_date: date) -> List[Room]:
        """

        :return:
        """

    @abstractmethod
    async def get_between_dates(self, start_date: date, end_date: date) -> List[Reservation]:
        """The method getting reservations made between provided start_date and end_date

        Args:
            start_date (date): The start date
            end_date (date): The end date

        Returns:
            List[Reservation]: The reservations made between the dates
        """

    @abstractmethod
    async def get_by_month(self, year: int, month_number: int) -> List[Reservation]:
        """The method getting reservations made in the provided month

        Args:
            month_number (int): The month number

        Returns:
            List[Reservation]: The reservations made in provided month
        """

    @abstractmethod
    async def get_by_year(self, year: int) -> List[Reservation]:
        """The method getting reservations made in the provided year

        Args:
            month_number (int): The year

        Returns:
            List[Reservation]: The reservations made in provided year
        """

    @abstractmethod
    async def add_reservation(self, data: ReservationIn) -> Reservation | None:
        """The method adding new reservation to the data storage.

        Args:
            data (reservationIn): The details of the new reservation.

        Returns:
            reservation | None: Full details of the newly added reservation.
        """

    @abstractmethod
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

    @abstractmethod
    async def delete_reservation(self, reservation_id: int) -> bool:
        """The method updating removing reservation from the data storage.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            bool: Success of the operation.
        """