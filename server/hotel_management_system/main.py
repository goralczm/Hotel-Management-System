"""
Main module of the app
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from hotel_management_system.api.routers.guest_accessibility_option_router import router as guest_accessibility_option_router
from hotel_management_system.api.routers.room_accessibility_option_router import router as room_accessibility_option_router
from hotel_management_system.api.routers.accessibility_option_router import router as accessibility_option_router
from hotel_management_system.api.routers.guest_router import router as guest_router
from hotel_management_system.api.routers.reservation_room_router import router as reservation_room_router
from hotel_management_system.api.routers.reservation_router import router as reservation_router
from hotel_management_system.api.routers.room_router import router as room_router
from hotel_management_system.api.routers.pricing_detail_router import router as pricing_detail_router
from hotel_management_system.api.routers.bill_router import router as bill_router
from hotel_management_system.api.routers.invoice_router import router as invoice_router
from hotel_management_system.api.routers.raport_router import raport_router as raport_router
from hotel_management_system.container import Container
from hotel_management_system.db import database
from hotel_management_system.db import init_db
from hotel_management_system.utils import setup

container = Container()
container.wire(modules=[
    "hotel_management_system.api.routers.guest_router",
    "hotel_management_system.api.routers.accessibility_option_router",
    "hotel_management_system.api.routers.room_router",
    "hotel_management_system.api.routers.room_accessibility_option_router",
    "hotel_management_system.api.routers.guest_accessibility_option_router",
    "hotel_management_system.api.routers.reservation_router",
    "hotel_management_system.api.routers.reservation_room_router",
    "hotel_management_system.api.routers.pricing_detail_router",
    "hotel_management_system.api.routers.bill_router",
    "hotel_management_system.api.routers.invoice_router",
    "hotel_management_system.api.routers.raport_router",
    "hotel_management_system.utils.setup",
])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """
    Lifespan function working on app startup.
    """
    await init_db()
    await database.connect()
    await setup.main()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(guest_router, prefix="/guest")
app.include_router(accessibility_option_router, prefix="/accessibility_option")
app.include_router(room_router, prefix="/room")
app.include_router(room_accessibility_option_router, prefix="/room_accessibility_option")
app.include_router(guest_accessibility_option_router, prefix="/guest_accessibility_option")
app.include_router(reservation_router, prefix="/reservation")
app.include_router(reservation_room_router, prefix="/reservation_room")
app.include_router(pricing_detail_router, prefix="/pricing_detail")
app.include_router(bill_router, prefix="/bill")
app.include_router(invoice_router, prefix="/invoice")
app.include_router(raport_router, prefix="/raport")
