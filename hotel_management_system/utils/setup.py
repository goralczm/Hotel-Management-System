from dependency_injector.wiring import Provide

from hotel_management_system.api.routers import reservation_router
from hotel_management_system.container import Container
from hotel_management_system.core.domains.accessibility_option import AccessibilityOptionIn
from hotel_management_system.core.domains.guest import GuestIn
from hotel_management_system.core.domains.guest_accessibility_option import GuestAccessibilityOptionIn
from hotel_management_system.core.domains.pricing_detail import PricingDetailIn
from hotel_management_system.core.domains.reservation import ReservationIn
from hotel_management_system.core.domains.room import RoomIn
from hotel_management_system.core.domains.room_accessibility_option import RoomAccessibilityOptionIn

from hotel_management_system.core.services.i_accessibility_option_service import IAccessibilityOptionService
from hotel_management_system.core.services.i_guest_accessibility_option_service import IGuestAccessibilityOptionService
from hotel_management_system.core.services.i_guest_service import IGuestService
from hotel_management_system.core.services.i_pricing_detail_service import IPricingDetailService
from hotel_management_system.core.services.i_reservation_service import IReservationService
from hotel_management_system.core.services.i_room_accessibility_option_service import IRoomAccessibilityOptionService
from hotel_management_system.core.services.i_room_service import IRoomService


async def main(
        accessibility_option_service: IAccessibilityOptionService = Provide[Container.accessibility_option_service],
        pricing_detail_service: IPricingDetailService = Provide[Container.pricing_detail_service],
        room_service: IRoomService = Provide[Container.room_service],
        guest_service: IGuestService = Provide[Container.guest_service],
        reservation_service: IReservationService = Provide[Container.reservation_service],
        room_accessibility_option_service: IRoomAccessibilityOptionService = Provide[Container.room_accessibility_option_service],
        guest_accessibility_option_service: IGuestAccessibilityOptionService = Provide[Container.guest_accessibility_option_service],
):
    await pricing_detail_service.add_pricing_detail(PricingDetailIn(
        name="Wczesne zameldowanie",
        price=25.00
    ))

    await pricing_detail_service.add_pricing_detail(PricingDetailIn(
        name="Śnidananie do pokoju",
        price=45.00
    ))

    sample_pricing_detail = await pricing_detail_service.add_pricing_detail(PricingDetailIn(
        name="Doba hotelowa",
        price=200.00
    ))

    sample_accessibility_option_1 = await accessibility_option_service.add_accessibility_option(AccessibilityOptionIn(
        name="Bezpierzowy"
    ))

    sample_accessibility_option_2 = await accessibility_option_service.add_accessibility_option(AccessibilityOptionIn(
        name="Niepalący"
    ))

    sample_guest = await guest_service.add_guest(GuestIn(
        first_name="John",
        last_name="Doe",
        address="123 Elm Street",
        city="Springfield",
        country="USA",
        zip_code="12345",
        phone_number="+1-555-1234",
        email="john.doe@example.com"
    ))

    await guest_accessibility_option_service.add_guest_accessibility_option(GuestAccessibilityOptionIn(
        guest_id=sample_guest.id,
        accessibility_option_id=sample_accessibility_option_1.id
    ))

    await guest_accessibility_option_service.add_guest_accessibility_option(GuestAccessibilityOptionIn(
        guest_id=sample_guest.id,
        accessibility_option_id=sample_accessibility_option_2.id
    ))

    sample_room_1 = await room_service.add_room(RoomIn(
        alias="A1"
    ))

    sample_room_2 = await room_service.add_room(RoomIn(
        alias="A2"
    ))

    await room_service.add_room(RoomIn(
        alias="A3"
    ))

    await room_accessibility_option_service.add_room_accessibility_option(RoomAccessibilityOptionIn(
        room_id=sample_room_1.id,
        accessibility_option_id=sample_accessibility_option_1.id
    ))

    await room_accessibility_option_service.add_room_accessibility_option(RoomAccessibilityOptionIn(
        room_id=sample_room_2.id,
        accessibility_option_id=sample_accessibility_option_1.id
    ))

    await room_accessibility_option_service.add_room_accessibility_option(RoomAccessibilityOptionIn(
        room_id=sample_room_2.id,
        accessibility_option_id=sample_accessibility_option_2.id
    ))

    await reservation_router.create_best_reservation(ReservationIn(
        guest_id=sample_guest.id,
        start_date="2024-12-17",
        end_date="2024-12-17"
    ), 1)
