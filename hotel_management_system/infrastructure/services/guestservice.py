"""Module containing continent service implementation."""

from typing import Iterable

from hotel_management_system.core.domains.guest import Guest, GuestIn
from hotel_management_system.core.repositories.iguestrepository import IGuestRepository
from hotel_management_system.infrastructure.dtos.guestdto import GuestDTO
from hotel_management_system.infrastructure.services.iguestservice import IGuestService


class GuestService(IGuestService):
    """A class implementing the guest service."""

    _repository: IGuestRepository

    def __init__(self, repository: IGuestRepository) -> None:
        """The initializer of the `guest service`.

        Args:
            repository (IguestRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[GuestDTO]:
        """The method getting all guests from the repository.

        Returns:
            Iterable[guestDTO]: All guests.
        """

        return await self._repository.get_all_guests()

    async def get_by_id(self, guest_id: int) -> GuestDTO | None:
        """The method getting guest by provided id.

        Args:
            guest_id (int): The id of the guest.

        Returns:
            guestDTO | None: The guest details.
        """

        return await self._repository.get_by_id(guest_id)

    async def add_guest(self, data: GuestIn) -> Guest | None:
        """The method adding new guest to the data storage.

        Args:
            data (guestIn): The details of the new guest.

        Returns:
            guest | None: Full details of the newly added guest.
        """

        return await self._repository.add_guest(data)

    async def update_guest(
            self,
            guest_id: int,
            data: GuestIn,
    ) -> Guest | None:
        """The method updating guest data in the data storage.

        Args:
            guest_id (int): The id of the guest.
            data (guestIn): The details of the updated guest.

        Returns:
            guest | None: The updated guest details.
        """

        return await self._repository.update_guest(
            guest_id=guest_id,
            data=data,
        )

    async def delete_guest(self, guest_id: int) -> bool:
        """The method updating removing guest from the data storage.

        Args:
            guest_id (int): The id of the guest.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_guest(guest_id)
