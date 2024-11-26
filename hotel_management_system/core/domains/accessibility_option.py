"""Module containing airport-related domain models"""
from asyncpg import Record
from pydantic import BaseModel, ConfigDict


class AccessibilityOptionIn(BaseModel):
    """Model representing guest's DTO attributes."""
    name: str

    @classmethod
    def from_dict(cls, data: dict) -> "AccessibilityOptionIn":
        return cls(
            name=data.get("name")
        )


class AccessibilityOption(AccessibilityOptionIn):
    """Model representing guest's attributes in the database."""
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )

    @classmethod
    def from_record(cls, record: Record) -> "AccessibilityOption":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            GuestDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            name=record_dict.get("name"),
        )
