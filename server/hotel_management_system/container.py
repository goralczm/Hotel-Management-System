"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from hotel_management_system.infrastructure.repositories.bill_repository import BillRepository
from hotel_management_system.infrastructure.repositories.guest_accessibility_option_repository import \
    GuestAccessibilityOptionRepository
from hotel_management_system.infrastructure.repositories.guest_repository import \
    GuestRepository
from hotel_management_system.infrastructure.repositories.invoice_repository import InvoiceRepository
from hotel_management_system.infrastructure.repositories.pricing_detail_repository import PricingDetailRepository
from hotel_management_system.infrastructure.repositories.reservation_repository import ReservationRepository
from hotel_management_system.infrastructure.repositories.reservation_room_repository import ReservationRoomRepository
from hotel_management_system.infrastructure.repositories.room_repository import RoomRepository
from hotel_management_system.infrastructure.services.bill_service import BillService
from hotel_management_system.infrastructure.services.guest_accessibility_option_service import \
    GuestAccessibilityOptionService
from hotel_management_system.infrastructure.services.guest_service import GuestService
from hotel_management_system.infrastructure.repositories.accessibility_option_repository import \
    AccessibilityOptionRepository
from hotel_management_system.infrastructure.services.accessibility_option_service import \
    AccessibilityOptionService
from hotel_management_system.infrastructure.services.invoice_service import InvoiceService
from hotel_management_system.infrastructure.services.pricing_detail_service import PricingDetailService
from hotel_management_system.infrastructure.services.reservation_room_service import ReservationRoomService
from hotel_management_system.infrastructure.services.reservation_service import ReservationService
from hotel_management_system.infrastructure.services.room_service import RoomService
from hotel_management_system.infrastructure.repositories.room_accessibility_option_repository import \
    RoomAccessibilityOptionRepository
from hotel_management_system.infrastructure.services.room_accessibility_option_service import \
    RoomAccessibilityOptionService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    guest_repository = Singleton(GuestRepository)
    accessibility_option_repository = Singleton(AccessibilityOptionRepository)
    room_repository = Singleton(RoomRepository)
    room_accessibility_option_repository = Singleton(RoomAccessibilityOptionRepository)
    guest_accessibility_option_repository = Singleton(GuestAccessibilityOptionRepository)
    reservation_repository = Singleton(ReservationRepository)
    reservation_room_repository = Singleton(ReservationRoomRepository)
    pricing_detail_repository = Singleton(PricingDetailRepository)
    bill_repository = Singleton(BillRepository)
    invoice_repository = Singleton(InvoiceRepository)

    guest_service = Factory(
        GuestService,
        guest_repository=guest_repository,
        accessibility_option_repository=accessibility_option_repository,
        guest_accessibility_option_repository=guest_accessibility_option_repository,
    )

    accessibility_option_service = Factory(
        AccessibilityOptionService,
        repository=accessibility_option_repository,
    )

    reservation_room_service = Factory(
        ReservationRoomService,
        repository=reservation_room_repository
    )

    room_service = Factory(
        RoomService,
        room_repository=room_repository,
        room_accessibility_option_repository=room_accessibility_option_repository,
        accessibility_option_repository=accessibility_option_repository,
        reservation_room_service=reservation_room_service,
    )

    room_accessibility_option_service = Factory(
        RoomAccessibilityOptionService,
        repository=room_accessibility_option_repository
    )

    guest_accessibility_option_service = Factory(
        GuestAccessibilityOptionService,
        repository=guest_accessibility_option_repository
    )

    bill_service = Factory(
        BillService,
        bill_repository=bill_repository,
        pricing_detail_repository=pricing_detail_repository
    )

    reservation_service = Factory(
        ReservationService,
        reservation_repository=reservation_repository,
        reservation_room_service=reservation_room_service,
        guest_service=guest_service,
        room_service=room_service,
        bill_service=bill_service
    )

    pricing_detail_service = Factory(
        PricingDetailService,
        repository=pricing_detail_repository
    )

    invoice_service = Factory(
        InvoiceService,
        invoice_repository=invoice_repository,
        reservation_service=reservation_service
    )
