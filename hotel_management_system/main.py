"""Main module of the app"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from hotel_management_system.api.routers.guest import router as guest_router
from hotel_management_system.container import Container
from hotel_management_system.db import database
from hotel_management_system.db import init_db

container = Container()
container.wire(modules=[
    "hotel_management_system.api.routers.guest",
])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(guest_router, prefix="/guest")