"""Module containing airport-related domain models"""

from typing import Optional

from asyncpg import Record
from pydantic import BaseModel, ConfigDict


class BillIn(BaseModel):
    """Model representing bill's DTO attributes."""
    room_id: int
    pricing_detail_id: int
    reservation_id: int


class Bill(BillIn):
    """Model representing bill's attributes in the database."""

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )

    @classmethod
    def from_record(cls, record: Record) -> "Bill":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            RoomAccessibilityDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            room_id=record_dict.get("room_id"),  # type: ignore
            pricing_detail_id=record_dict.get("pricing_detail_id"),
            reservation_id=record_dict.get("reservation_id")
        )
