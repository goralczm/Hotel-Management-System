"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from hotel_management_system.infrastructure.repositories.guestdb import \
    GuestRepository
from hotel_management_system.infrastructure.services.guestservice import GuestService

class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    guest_repository = Singleton(GuestRepository)

    guest_service = Factory(
        GuestService,
        repository=guest_repository,
    )