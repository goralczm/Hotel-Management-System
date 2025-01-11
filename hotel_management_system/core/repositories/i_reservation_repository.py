"""Module containing reservation repository abstractions."""

from abc import ABC, abstractmethod
from datetime import date
from typing import List

from hotel_management_system.core.domains.reservation import ReservationIn, Reservation


class IReservationRepository(ABC):
    """An abstract class representing protocol of continent repository."""

    @abstractmethod
    async def get_all_reservations(self) -> List[Reservation]:
        """The abstract getting all reservations from the data storage.

        Returns:
            List[Reservation]: Reservations in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, reservation_id: int) -> Reservation | None:
        """The method getting reservation by provided id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Reservation | None: The reservation details.
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
    async def add_reservation(self, data: ReservationIn) -> Reservation | None:
        """The abstract adding new reservation to the data storage.

        Args:
            data (ReservationIn): The details of the new reservation.

        Returns:
            Reservation | None: The newly added reservation.
        """

    @abstractmethod
    async def update_reservation(
            self,
            reservation_id: int,
            data: ReservationIn,
    ) -> Reservation | None:
        """The abstract updating reservation data in the data storage.

        Args:
            reservation_id (int): The id of the reservation.
            data (ReservationIn): The details of the updated reservation.

        Returns:
            Reservation | None: The updated reservation details.
        """

    @abstractmethod
    async def delete_reservation(self, reservation_id: int) -> bool:
        """The abstract updating removing reservation from the data storage.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            bool: Success of the operation.
        """