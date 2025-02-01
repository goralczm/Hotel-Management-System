from asyncpg import Record
from pydantic import BaseModel, ConfigDict


class PricingDetailIn(BaseModel):
    """Model representing the input DTO for creating or updating pricing details."""
    name: str
    price: float


class PricingDetail(PricingDetailIn):
    """Model representing pricing details' attributes in the database."""
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

    @classmethod
    def from_record(cls, record: Record) -> "PricingDetail":
        """Convert a database record into a PricingDetail instance.

        Args:
            record (Record): The DB record.

        Returns:
            PricingDetail: The DTO instance populated with the data from the DB record.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            name=record_dict.get("name"),
            price=record_dict.get("price"),
        )
