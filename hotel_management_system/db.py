"""A module providing database access."""

import asyncio

import databases
import sqlalchemy
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)

from hotel_management_system.config import config

metadata = sqlalchemy.MetaData()

guests_table = sqlalchemy.Table(
    "guests",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("address", sqlalchemy.String),
    sqlalchemy.Column("city", sqlalchemy.String),
    sqlalchemy.Column("country", sqlalchemy.String),
    sqlalchemy.Column("zip_code", sqlalchemy.String),
    sqlalchemy.Column("phone_number", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
)

rooms_table = sqlalchemy.Table(
    "rooms",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("alias", sqlalchemy.String),
)

reservations_table = sqlalchemy.Table(
    "reservations",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("guest_id", sqlalchemy.ForeignKey("guests.id"), nullable=False),
    sqlalchemy.Column("start_date", sqlalchemy.Date),
    sqlalchemy.Column("end_date", sqlalchemy.Date)
)

reservation_rooms_table = sqlalchemy.Table(
    "reservation_rooms",
    metadata,
    sqlalchemy.Column("reservation_id", sqlalchemy.ForeignKey("reservations.id"), nullable=False),
    sqlalchemy.Column("room_id", sqlalchemy.ForeignKey("rooms.id"), nullable=False)
)

db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(
    db_uri,
    force_rollback=True,
)


async def init_db(retries: int = 5, delay: int = 5) -> None:
    """Function initializing the DB.

    Args:
        retries (int, optional): Number of retries of connect to DB.
            Defaults to 5.
        delay (int, optional): Delay of connect do DB. Defaults to 2.
    """
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            return
        except (
                OperationalError,
                DatabaseError,
                CannotConnectNowError,
                ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")