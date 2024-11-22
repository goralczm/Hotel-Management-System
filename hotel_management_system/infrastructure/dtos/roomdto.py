"""A module containing DTO models for output airports."""


from typing import Optional
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict

class RoomDTO(BaseModel):
    """A model representing DTO for airport data."""
    id: int
    alias: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "RoomDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            AirportDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            alias=record_dict.get("alias")
        )