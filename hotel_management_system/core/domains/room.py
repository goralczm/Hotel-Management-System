"""Module containing airport-related domain models"""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class RoomIn(BaseModel):
    """Model representing airport's DTO attributes."""
    alias: str

class Room(RoomIn):
    """Model representing airport's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
