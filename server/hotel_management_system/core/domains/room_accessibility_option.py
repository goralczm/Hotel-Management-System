"""Module containing airport-related domain models"""

from typing import Optional

from asyncpg import Record
from pydantic import BaseModel, ConfigDict


class RoomAccessibilityOptionIn(BaseModel):
    """Model representing room_accessibility's DTO attributes."""
    room_id: int
    accessibility_option_id: int


class RoomAccessibilityOption(RoomAccessibilityOptionIn):
    """Model representing room_accessibility's attributes in the database."""

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )

    @classmethod
    def from_record(cls, record: Record) -> "RoomAccessibilityOption":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            RoomAccessibilityOption: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            room_id=record_dict.get("room_id"),
            accessibility_option_id=record_dict.get("accessibility_option_id"),
        )
