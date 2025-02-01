"""Module containing airport-related domain models"""

from typing import Optional, List

from asyncpg import Record
from pydantic import BaseModel, ConfigDict

from hotel_management_system.core.domains.accessibility_option import AccessibilityOption


class GuestIn(BaseModel):
    """Model representing guest's DTO attributes."""
    first_name: str
    last_name: str
    address: str
    city: str
    country: str
    zip_code: str
    phone_number: str
    email: str


class Guest(GuestIn):
    """Model representing guest's attributes in the database."""
    id: int
    accessibility_options: List[AccessibilityOption] = []

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

    @classmethod
    def from_record(cls, record: Record) -> "Guest":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            GuestDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            first_name=record_dict.get("first_name"),
            last_name=record_dict.get("last_name"),
            address=record_dict.get("address"),
            city=record_dict.get("city"),
            country=record_dict.get("country"),
            zip_code=record_dict.get("zip_code"),
            phone_number=record_dict.get("phone_number"),
            email=record_dict.get("email"),
        )
