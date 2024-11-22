"""A module containing DTO models for output airports."""


from typing import Optional
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict

class GuestDTO(BaseModel):
    """A model representing DTO for airport data."""
    id: int
    first_name: str
    last_name: str
    address: str
    city: str
    country: str
    zip_code: str
    phone_number: str
    email: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "GuestDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            AirportDTO: The final DTO instance.
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