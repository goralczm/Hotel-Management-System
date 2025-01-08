"""Module containing airport-related domain models"""
import datetime
from typing import Optional, List

from asyncpg import Record
from pydantic import BaseModel, ConfigDict

from hotel_management_system.core.domains.bill import Bill
from hotel_management_system.core.domains.room import Room


class ReservationIn(BaseModel):
    """Model representing reservation's DTO attributes."""
    guest_id: int
    start_date: datetime.date
    end_date: datetime.date
    number_of_guests: int


class Reservation(ReservationIn):
    """Model representing reservation's attributes in the database."""
    id: int
    reserved_rooms: List[Room] = []
    bills: List[Bill] = []

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )

    @classmethod
    def from_record(cls, record: Record) -> "Reservation":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ReservationDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            guest_id=record_dict.get("guest_id"),
            start_date=record_dict.get("start_date"),
            end_date=record_dict.get("end_date"),
            number_of_guests=record_dict.get("number_of_guests")
        )

    def get_cost(self) -> float:
        cost = 0.0
        for bill in self.bills:
            cost += bill.pricing_detail.price

        return cost
