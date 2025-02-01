from asyncpg import Record
from pydantic import BaseModel, ConfigDict

from hotel_management_system.core.domains.pricing_detail import PricingDetail


class BillIn(BaseModel):
    """Model representing the input DTO for creating or updating a bill."""
    room_id: int
    pricing_detail_id: int
    reservation_id: int


class Bill(BillIn):
    """Model representing the bill's attributes in the database."""
    pricing_detail: PricingDetail = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )

    @classmethod
    def from_record(cls, record: Record) -> "Bill":
        """Convert a DB record into a Bill instance.

        Args:
            record (Record): A record fetched from the database.

        Returns:
            Bill: The model instance populated with the data from the DB record.
        """
        record_dict = dict(record)

        return cls(
            room_id=record_dict.get("room_id"),
            pricing_detail_id=record_dict.get("pricing_detail_id"),
            reservation_id=record_dict.get("reservation_id"),
        )
