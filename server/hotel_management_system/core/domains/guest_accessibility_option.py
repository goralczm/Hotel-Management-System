from asyncpg import Record
from pydantic import BaseModel, ConfigDict


class GuestAccessibilityOptionIn(BaseModel):
    """Model representing the input DTO for creating or updating a guest's accessibility option."""
    guest_id: int
    accessibility_option_id: int

    @classmethod
    def from_dict(cls, data: dict) -> "GuestAccessibilityOptionIn":
        """Convert a dictionary into a GuestAccessibilityOptionIn instance.

        Args:
            data (dict): A dictionary containing the attributes to initialize the model.

        Returns:
            GuestAccessibilityOptionIn: The corresponding model instance.
        """
        return cls(
            guest_id=data.get("guest_id"),
            accessibility_option_id=data.get("accessibility_option_id"),
        )


class GuestAccessibilityOption(GuestAccessibilityOptionIn):
    """Model representing the guest's accessibility option attributes in the database."""

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

    @classmethod
    def from_record(cls, record: Record) -> "GuestAccessibilityOption":
        """Convert a DB record into a GuestAccessibilityOption instance.

        Args:
            record (Record): A record fetched from the database.

        Returns:
            GuestAccessibilityOption: The model instance populated with the data from the DB record.
        """
        record_dict = dict(record)

        return cls(
            guest_id=record_dict.get("guest_id"),
            accessibility_option_id=record_dict.get("accessibility_option_id"),
        )
