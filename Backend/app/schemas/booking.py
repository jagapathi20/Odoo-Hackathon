from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from typing import Optional, List
from app.utils.enums import BookingStatus
import re

class BookingBase(BaseModel):
    resource_id: UUID
    date: str = Field(..., example="2026-07-12")  # ISO format date matching current project window
    start_time: str = Field(..., example="09:30")  # HH:MM format
    end_time: str = Field(..., example="10:30")    # HH:MM format

    @field_validator('start_time', 'end_time')
    @classmethod
    def validate_time_format(cls, value: str) -> str:
        if not re.match(r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$", value):
            raise ValueError("Time must be in HH:MM 24-hour format")
        return value

class BookingCreate(BookingBase):
    purpose: Optional[str] = Field(None, max_length=255)

class BookingReschedule(BaseModel):
    date: str = Field(..., example="2026-07-13")
    start_time: str = Field(..., example="10:00")
    end_time: str = Field(..., example="11:00")

# Struct representing individual resource slots in day-grid view
class BookingSlotOut(BaseModel):
    start: str
    end: str
    status: str  # BOOKED or FREE
    booked_by: Optional[str] = None

class ResourceMinOut(BaseModel):
    id: UUID
    name: str

class BookingGridResponse(BaseModel):
    resource: ResourceMinOut
    date: str
    slots: List[BookingSlotOut]

class BookingOut(BookingBase):
    id: UUID
    status: BookingStatus
    purpose: Optional[str] = None

    class Config:
        from_attributes = True