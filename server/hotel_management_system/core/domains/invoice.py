import datetime
from asyncpg import Record
from pydantic import BaseModel, ConfigDict
from hotel_management_system.core.domains.reservation import Reservation


class InvoiceIn(BaseModel):
    """Model representing the input DTO for creating or updating an invoice."""
    date_of_issue: datetime.date
    first_name: str
    last_name: str
    address: str
    nip: str
    reservation_id: int


class Invoice(InvoiceIn):
    """Model representing an invoice's attributes in the database."""
    id: int
    total_sum: float = 0.0
    reservation: Reservation = None
    company_name: str = "Hotel Felix"
    company_address: str = "ul. Słoneczna 15, 00-123 Warszawa"
    company_nip: str = "123-456-78-90"
    company_phone: str = "+48 221 234 567"
    company_email: str = "recepcja@hotelfelix.pl"

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

    @classmethod
    def from_record(cls, record: Record) -> "Invoice":
        """Convert a DB record into an Invoice instance.

        Args:
            record (Record): A record fetched from the database.

        Returns:
            Invoice: The model instance populated with the data from the DB record.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            date_of_issue=record_dict.get("date_of_issue"),
            first_name=record_dict.get("first_name"),
            last_name=record_dict.get("last_name"),
            address=record_dict.get("address"),
            nip=record_dict.get("nip"),
            reservation_id=record_dict.get("reservation_id"),
            total_sum=record_dict.get("total_sum", 0.0),
        )
