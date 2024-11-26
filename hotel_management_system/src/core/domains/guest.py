"""Module containing airport-related domain models"""

from typing import Optional

from asyncpg import Record
from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
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
            id=record_dict.get("id"),  # type: ignore
            first_name=record_dict.get("first_name"),
            last_name=record_dict.get("last_name"),  # type: ignore
            address=record_dict.get("address"),  # type: ignore
            city=record_dict.get("city"),  # type: ignore
            country=record_dict.get("country"),  # type: ignore
            zip_code=record_dict.get("zip_code"),  # type: ignore
            phone_number=record_dict.get("phone_number"),  # type: ignore
            email=record_dict.get("email")
        )
