"""Module containing airport-related domain models"""

from typing import Optional

from asyncpg import Record
from pydantic import BaseModel, ConfigDict


class PricingDetailIn(BaseModel):
    """Model representing pricing_detail's DTO attributes."""
    name: str
    price: float

    @classmethod
    def from_dict(cls, data: dict) -> "PricingDetailIn":
        return cls(
            name=data.get("name"),
            price=data.get("price"),
        )


class PricingDetail(PricingDetailIn):
    """Model representing pricing_detail's attributes in the database."""
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )

    @classmethod
    def from_record(cls, record: Record) -> "PricingDetail":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            PricingDetailDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            name=record_dict.get("name"),
            price=record_dict.get("price"),
        )
