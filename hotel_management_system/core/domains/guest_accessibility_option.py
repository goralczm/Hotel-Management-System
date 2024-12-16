"""Module containing airport-related domain models"""

from typing import Optional

from asyncpg import Record
from pydantic import BaseModel, ConfigDict


class GuestAccessibilityOptionIn(BaseModel):
    """Model representing guest_accessibility's DTO attributes."""
    guest_id: int
    accessibility_option_id: int


class GuestAccessibilityOption(GuestAccessibilityOptionIn):
    """Model representing guest_accessibility's attributes in the database."""

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )

    @classmethod
    def from_record(cls, record: Record) -> "GuestAccessibilityOption":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            GuestAccessibilityDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            guest_id=record_dict.get("guest_id"),  # type: ignore
            accessibility_option_id=record_dict.get("accessibility_option_id")
        )
