"""
Module for managing reservation repository abstractions.
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import List

from hotel_management_system.core.domains.reservation import ReservationIn, Reservation


class IReservationRepository(ABC):
    """
    Abstract base class defining the interface for a reservation repository.
    """

    @abstractmethod
    async def get_all_reservations(self) -> List[Reservation]:
        """
        Retrieve all reservations from the data storage.

        Returns:
            List[Reservation]: A list of all reservations.
        """

    @abstractmethod
    async def get_by_id(self, reservation_id: int) -> Reservation | None:
        """
        Retrieve a reservation by its unique ID.

        Args:
            reservation_id (int): The ID of the reservation.

        Returns:
            Reservation | None: The details of the reservation if found, or None if not found.
        """

    @abstractmethod
    async def get_between_dates(self, start_date: date, end_date: date) -> List[Reservation]:
        """
        Retrieve reservations made between the provided start and end dates.

        Args:
            start_date (date): The start date of the range.
            end_date (date): The end date of the range.

        Returns:
            List[Reservation]: A list of reservations made within the date range.
        """

    @abstractmethod
    async def get_by_month(self, year: int, month_number: int) -> List[Reservation]:
        """
        Retrieve reservations made during the specified month.

        Args:
            year (int): The year of the reservations.
            month_number (int): The month number (1 for January, 12 for December).

        Returns:
            List[Reservation]: A list of reservations made in the specified month.
        """

    @abstractmethod
    async def add_reservation(self, data: ReservationIn) -> Reservation | None:
        """
        Add a new reservation to the data storage.

        Args:
            data (ReservationIn): The details of the new reservation.

        Returns:
            Reservation | None: The newly added reservation, or None if the operation fails.
        """

    @abstractmethod
    async def update_reservation(self, reservation_id: int, data: ReservationIn) -> Reservation | None:
        """
        Update the details of an existing reservation in the data storage.

        Args:
            reservation_id (int): The ID of the reservation to update.
            data (ReservationIn): The updated details for the reservation.

        Returns:
            Reservation | None: The updated reservation details, or None if the reservation is not found.
        """

    @abstractmethod
    async def delete_reservation(self, reservation_id: int) -> bool:
        """
        Remove a reservation from the data storage.

        Args:
            reservation_id (int): The ID of the reservation to remove.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
