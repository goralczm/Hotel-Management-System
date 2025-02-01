from asyncpg import Record
from pydantic import BaseModel, ConfigDict


class AccessibilityOptionIn(BaseModel):
    """Model representing the DTO for creating or updating an accessibility option."""
    name: str


class AccessibilityOption(AccessibilityOptionIn):
    """Model representing an accessibility option as stored in the database."""
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

    @classmethod
    def from_record(cls, record: Record) -> "AccessibilityOption":
        """Convert a DB record into an AccessibilityOption instance.

        Args:
            record (Record): A record fetched from the database.

        Returns:
            AccessibilityOption: The model instance populated with the data from the DB record.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            name=record_dict.get("name"),
        )
