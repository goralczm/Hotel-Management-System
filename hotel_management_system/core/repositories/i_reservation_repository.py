"""Module containing reservation repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from hotel_management_system.core.domains.reservation import ReservationIn


class IReservationRepository(ABC):
    """An abstract class representing protocol of continent repository."""

    @abstractmethod
    async def get_all_reservations(self) -> Iterable[Any]:
        """The abstract getting all reservations from the data storage.

        Returns:
            Iterable[Any]: Reservations in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, reservation_id: int) -> Any | None:
        """The method getting reservation by provided id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Any | None: The reservation details.
        """

    @abstractmethod
    async def add_reservation(self, data: ReservationIn) -> Any | None:
        """The abstract adding new reservation to the data storage.

        Args:
            data (ReservationIn): The details of the new reservation.

        Returns:
            Any | None: The newly added reservation.
        """

    @abstractmethod
    async def update_reservation(
            self,
            reservation_id: int,
            data: ReservationIn,
    ) -> Any | None:
        """The abstract updating reservation data in the data storage.

        Args:
            reservation_id (int): The id of the reservation.
            data (ReservationIn): The details of the updated reservation.

        Returns:
            Any | None: The updated reservation details.
        """

    @abstractmethod
    async def delete_reservation(self, reservation_id: int) -> bool:
        """The abstract updating removing reservation from the data storage.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            bool: Success of the operation.
        """