"""Module containing room-related domain models"""
from typing import List

from asyncpg import Record
from pydantic import BaseModel, ConfigDict

from hotel_management_system.core.domains.accessibility_option import AccessibilityOption


class RoomIn(BaseModel):
    """Model representing room's DTO attributes."""
    alias: str


class Room(RoomIn):
    """Model representing room's attributes in the database."""
    id: int
    accessibility_options: List[AccessibilityOption] = []

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

    @classmethod
    def from_record(cls, record: Record) -> "Room":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            Room: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            alias=record_dict.get("alias"),
        )

    def correlation_coefficient(self, accessibility_options: List[AccessibilityOption]) -> int:
        """Calculates a coefficient based on matched accessibility options.

        Args:
            accessibility_options (List[AccessibilityOption]): List of options to compare.

        Returns:
            int: The number of matched accessibility options.
        """
        coefficient = 0
        for accessibility_option in self.accessibility_options:
            if accessibility_option in accessibility_options:
                coefficient += 1

        return coefficient
