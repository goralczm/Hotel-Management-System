"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from hotel_management_system.src.infrastructure.repositories.guest_repository import \
    GuestRepository
from hotel_management_system.src.infrastructure.repositories.room_repository import RoomRepository
from hotel_management_system.src.infrastructure.services.guest_service import GuestService
from hotel_management_system.src.infrastructure.repositories.accessibility_option_repository import \
    AccessibilityOptionRepository
from hotel_management_system.src.infrastructure.services.accessibility_option_service import \
    AccessibilityOptionService
from hotel_management_system.src.infrastructure.services.room_service import RoomService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    guest_repository = Singleton(GuestRepository)
    accessibility_repository = Singleton(AccessibilityOptionRepository)
    room_repository = Singleton(RoomRepository)

    guest_service = Factory(
        GuestService,
        repository=guest_repository,
    )

    accessibility_option_service = Factory(
        AccessibilityOptionService,
        repository=accessibility_repository,
    )

    room_service = Factory(
        RoomService,
        repository=room_repository
    )
