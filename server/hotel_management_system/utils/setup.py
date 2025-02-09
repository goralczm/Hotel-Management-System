import os
import time
from datetime import datetime, timedelta

from dependency_injector.wiring import Provide
import random

from fastapi import HTTPException

from hotel_management_system.api.routers import reservation_router
from hotel_management_system.container import Container
from hotel_management_system.core.domains.accessibility_option import AccessibilityOptionIn
from hotel_management_system.core.domains.bill import BillIn
from hotel_management_system.core.domains.guest import GuestIn
from hotel_management_system.core.domains.guest_accessibility_option import GuestAccessibilityOptionIn
from hotel_management_system.core.domains.pricing_detail import PricingDetailIn
from hotel_management_system.core.domains.reservation import ReservationIn
from hotel_management_system.core.domains.room import RoomIn
from hotel_management_system.core.domains.room_accessibility_option import RoomAccessibilityOptionIn

from hotel_management_system.core.services.i_accessibility_option_service import IAccessibilityOptionService
from hotel_management_system.core.services.i_bill_service import IBillService
from hotel_management_system.core.services.i_guest_accessibility_option_service import IGuestAccessibilityOptionService
from hotel_management_system.core.services.i_guest_service import IGuestService
from hotel_management_system.core.services.i_pricing_detail_service import IPricingDetailService
from hotel_management_system.core.services.i_room_accessibility_option_service import IRoomAccessibilityOptionService
from hotel_management_system.core.services.i_room_service import IRoomService


def get_random_date():
    current_year = datetime.now().year

    current_year += random.randint(-1, 1)

    start_date = datetime(current_year, 1, 1)
    end_date = datetime(current_year, 12, 31)

    days_in_year = (end_date - start_date).days + 1

    random_days = random.randint(0, days_in_year - 1)

    random_date = start_date + timedelta(days=random_days)

    return random_date


async def main(
        accessibility_option_service: IAccessibilityOptionService = Provide[Container.accessibility_option_service],
        pricing_detail_service: IPricingDetailService = Provide[Container.pricing_detail_service],
        room_service: IRoomService = Provide[Container.room_service],
        guest_service: IGuestService = Provide[Container.guest_service],
        room_accessibility_option_service: IRoomAccessibilityOptionService = Provide[Container.room_accessibility_option_service],
        guest_accessibility_option_service: IGuestAccessibilityOptionService = Provide[Container.guest_accessibility_option_service],
        bill_service: IBillService = Provide[Container.bill_service],
):
    if os.environ.get('SETUP', 'False') == 'False':
        print('\n=== Setup skipped ===', flush=True)
        return

    print('\n=== Starting setup ===', flush=True)
    setup_start = time.time()
    start = time.time()
    pricing_details_data = (
        ("Doba hotelowa", 200.00),
        ("Wczesne zameldowanie", 25.00),
        ("Śniadanie do pokoju", 45.00),
    )

    sample_pricing_details = []
    for pricing_detail in pricing_details_data:
        sample_pricing_details.append(
            await pricing_detail_service.add_pricing_detail(
                PricingDetailIn(
                    name=pricing_detail[0],
                    price=pricing_detail[1],
                )
            )
        )
    end = time.time()
    print(f'Pricing details: {round(end - start, 2)} seconds', flush=True)

    start = time.time()
    accessibility_options_data = (
        "Pierwsze Piętro",
        "Drugie Piętro",
        "Bezpierzowy",
        "Niepalący",
        "Niskopodłogowy",
        "Wsparcie dla wózka",
    )

    sample_accessibility_options = []
    for accessibility_option in accessibility_options_data:
        sample_accessibility_options.append(
            await accessibility_option_service.add_accessibility_option(
                AccessibilityOptionIn(
                    name=accessibility_option
                )
            )
        )
    end = time.time()
    print(f'Accessibility options: {round(end - start, 2)} seconds', flush=True)

    start = time.time()
    sample_guests = []
    with open(os.path.join(os.path.dirname(__file__), 'random_contacts.csv'), 'r') as random_contacts:
        random_contacts = random_contacts.readlines()
        with open(os.path.join(os.path.dirname(__file__),'random_addresses.csv'), 'r') as random_addresses:
            random_addresses = random_addresses.readlines()

            guests_count = int(os.environ.get('SETUP_GUEST_COUNT', 100))
            for _ in range(guests_count):
                random_contact = random_contacts[random.randint(0, len(random_contacts) - 1)].split(',')
                random_address = random_addresses[random.randint(0, len(random_addresses) - 1)].split(',')

                random_guest = (
                    random_contact[0],
                    random_contact[1],
                    random_address[0],
                    random_address[1],
                    random_address[2],
                    random_address[3],
                    random_contact[2],
                    random_contact[3],
                )

                new_guest = await guest_service.add_guest(
                    GuestIn(
                        first_name=random_guest[0],
                        last_name=random_guest[1],
                        address=random_guest[2],
                        city=random_guest[3],
                        country=random_guest[4],
                        zip_code=random_guest[5],
                        phone_number=random_guest[6],
                        email=random_guest[7],
                    )
                )

                sample_guests.append(new_guest)

                has_accessibility_options = random.randint(0, 4) == 0
                if has_accessibility_options:
                    unused_accessibilities = sample_accessibility_options[:]

                    # Cannot have both first and second floor accessibility options
                    if random.randint(0, 1) == 0:
                        del unused_accessibilities[0]
                    else:
                        del unused_accessibilities[1]

                    for _ in range(0, random.randint(1, 4)):
                        accessibility_option = unused_accessibilities[random.randint(0, len(unused_accessibilities) - 1)]
                        unused_accessibilities.remove(accessibility_option)

                        await guest_accessibility_option_service.add_guest_accessibility_option(
                            GuestAccessibilityOptionIn(
                                guest_id=new_guest.id,
                                accessibility_option_id=accessibility_option.id,
                            )
                        )
    end = time.time()
    print(f'Guests: {round(end - start, 2)} seconds', flush=True)

    first_floor_accessibility_option = await accessibility_option_service.get_by_name("Pierwsze Piętro")
    second_floor_accessibility_option = await accessibility_option_service.get_by_name("Drugie Piętro")

    start = time.time()
    sample_rooms = []
    for i in range(2):
        for j in range(50):
            if i == 0:
                prefix = 'A'
                accessibility_option = first_floor_accessibility_option
            else:
                prefix = 'B'
                accessibility_option = second_floor_accessibility_option

            new_room = await room_service.add_room(
                RoomIn(
                    alias=f'{prefix}{j}'
                )
            )

            sample_rooms.append(new_room)

            await room_accessibility_option_service.add_room_accessibility_option(
                RoomAccessibilityOptionIn(
                    room_id=new_room.id,
                    accessibility_option_id=accessibility_option.id
                )
            )

            has_accessibility_options = random.randint(0, 4) == 0
            if has_accessibility_options:
                unused_accessibilities = sample_accessibility_options[2:]
                for _ in range(1, 4):
                    accessibility_option = unused_accessibilities[random.randint(0, len(unused_accessibilities) - 1)]
                    unused_accessibilities.remove(accessibility_option)
                    await room_accessibility_option_service.add_room_accessibility_option(
                        RoomAccessibilityOptionIn(
                            room_id=new_room.id,
                            accessibility_option_id=accessibility_option.id,
                        )
                    )

    end = time.time()
    print(f'Rooms: {round(end - start, 2)} seconds', flush=True)

    start = time.time()
    available_pricings = sample_pricing_details[1:]

    reservation_count = int(os.environ.get('SETUP_RESERVATION_COUNT', 10))
    for guest in sample_guests[:reservation_count]:
        random_start_date = get_random_date()
        days_staying = random.randint(1, 7)
        end_date = random_start_date + timedelta(days=days_staying)
        number_of_guests = random.randint(1, 6)

        new_reservation = None
        try:
            new_reservation = await reservation_router.create_best_reservation(
                ReservationIn(
                    guest_id=guest.id,
                    start_date=random_start_date.strftime('%Y-%m-%d'),
                    end_date=end_date.strftime('%Y-%m-%d'),
                    number_of_guests=number_of_guests
                ),
                max(1, number_of_guests // 2)
            )
        except HTTPException as error:
            print(f"CANNOT CREATE RESERVATION {random_start_date.strftime('%Y-%m-%d')}-{end_date.strftime('%Y-%m-%d')}: because {error}")
        else:
            if new_reservation and len(new_reservation.reserved_rooms) > 0:
                has_bought_something = random.randint(0, 1) == 0
                if has_bought_something:
                    random_pricing = available_pricings[random.randint(0, len(available_pricings) - 1)]
                    room_who_bought = new_reservation.reserved_rooms[
                        random.randint(0, len(new_reservation.reserved_rooms) - 1)
                    ]

                    await bill_service.add_bill(
                        BillIn(
                            room_id=room_who_bought.id,
                            pricing_detail_id=random_pricing.id,
                            reservation_id=new_reservation.id,
                        )
                    )
    end = time.time()
    setup_end = time.time()
    print(f'Reservations: {round(end - start, 2)} seconds', flush=True)
    print(f'=== Setup done: {round(setup_end - setup_start, 2)} seconds ===\n', flush=True)
