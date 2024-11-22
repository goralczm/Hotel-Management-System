"""Module containing airport-related domain models"""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class GuestIn(BaseModel):
    """Model representing airport's DTO attributes."""
    first_name: str
    last_name: str
    address: str
    city: str
    country: str
    zip_code: str
    phone_number: str
    email: str

class Guest(GuestIn):
    """Model representing airport's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
