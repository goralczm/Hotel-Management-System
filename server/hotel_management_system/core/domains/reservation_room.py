from asyncpg import Record
from pydantic import BaseModel, ConfigDict


class ReservationRoomIn(BaseModel):
    """Model representing reservation_room's DTO attributes."""
    reservation_id: int
    room_id: int


class ReservationRoom(ReservationRoomIn):
    """Model representing reservation_room's attributes in the database."""

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

    @classmethod
    def from_record(cls, record: Record) -> "ReservationRoom":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ReservationRoom: The final DTO instance.
        """

        record_dict = dict(record)

        return cls(
            reservation_id=record_dict.get("reservation_id"),
            room_id=record_dict.get("room_id"),
        )
