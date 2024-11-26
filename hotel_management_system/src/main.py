"""Main module of the app"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from hotel_management_system.src.api.routers.guest import router as guest_router
from hotel_management_system.src.api.routers.accessibility import router as accessibility_router
from hotel_management_system.src.api.routers.room import router as room_router
from hotel_management_system.src.container import Container
from hotel_management_system.src.db import database
from hotel_management_system.src.db import init_db
from hotel_management_system.src.utils import setup

container = Container()
container.wire(modules=[
    "hotel_management_system.api.routers.guest",
    "hotel_management_system.api.routers.accessibility",
    "hotel_management_system.api.routers.room",
    "hotel_management_system.utils.setup",
])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    await setup.main()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(guest_router, prefix="/guest")
app.include_router(accessibility_router, prefix="/accessibility_options")
app.include_router(room_router, prefix="/room")
