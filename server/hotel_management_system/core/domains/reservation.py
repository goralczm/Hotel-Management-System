import datetime
from typing import List

from asyncpg import Record
from pydantic import BaseModel, ConfigDict

from hotel_management_system.core.domains.bill import Bill
from hotel_management_system.core.domains.guest import Guest
from hotel_management_system.core.domains.room import Room


class ReservationIn(BaseModel):
    """Model representing the input DTO for creating or updating a reservation."""
    guest_id: int
    start_date: datetime.date
    end_date: datetime.date
    number_of_guests: int

    def get_duration(self) -> int:
        """Calculate the duration of the reservation in days."""
        return (self.end_date - self.start_date).days


class Reservation(ReservationIn):
    """Model representing the reservation's attributes in the database."""
    id: int
    guest: Guest = None
    reserved_rooms: List[Room] = []
    bills: List[Bill] = []

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

    @classmethod
    def from_record(cls, record: Record) -> "Reservation":
        """Prepare a Reservation instance based on the DB record.

        Args:
            record (Record): The DB record.

        Returns:
            Reservation: The final Reservation DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            guest_id=record_dict.get("guest_id"),
            start_date=record_dict.get("start_date"),
            end_date=record_dict.get("end_date"),
            number_of_guests=record_dict.get("number_of_guests"),
        )

    def get_cost(self) -> float:
        """Calculate the total cost for the reservation from linked bills."""
        cost = 0.0
        for bill in self.bills:
            if bill.pricing_detail:
                cost += bill.pricing_detail.price
        return cost
