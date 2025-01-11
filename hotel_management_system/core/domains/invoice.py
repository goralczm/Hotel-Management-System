"""Module containing airport-related domain models"""
import datetime

from asyncpg import Record
from pydantic import BaseModel, ConfigDict

from hotel_management_system.core.domains.reservation import Reservation


class InvoiceIn(BaseModel):
    """Model representing pricing_detail's DTO attributes."""
    date_of_issue: datetime.date
    first_name: str
    last_name: str
    address: str
    nip: str
    reservation_id: int
    company_name: str = "Hotel Felix"
    company_address: str = "ul. Słoneczna 15, 00-123 Warszawa"
    company_nip: str = "123-456-78-90"
    company_phone: str = "+48 221 234 567"
    company_email: str = "recepcja@hotelfelix.pl"

class Invoice(InvoiceIn):
    """Model representing pricing_detail's attributes in the database."""
    id: int
    total_sum: float = 0
    reservation: Reservation = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )

    @classmethod
    def from_record(cls, record: Record) -> "Invoice":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            InvoiceDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            date_of_issue=record_dict.get("date_of_issue"),
            first_name=record_dict.get("first_name"),
            last_name=record_dict.get("last_name"),
            address=record_dict.get("address"),
            nip=record_dict.get("nip"),
            reservation_id=record_dict.get("reservation_id"),
        )
