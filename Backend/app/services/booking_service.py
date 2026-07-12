from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status

from app.models.asset import Asset
from app.models.booking import Booking
from app.utils.enums import BookingStatus

def validate_and_create_booking(
    db: Session, resource_id: UUID, user_id: UUID, date: str, start: str, end: str, purpose: str = None
) -> Booking:
    """
    Evaluates requested time slots against current bookings.
    Rejects overlapping intervals while explicitly allowing back-to-back records.
    """
    resource = db.query(Asset).filter(Asset.id == resource_id, Asset.is_bookable == True).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found or not bookable")

    # Core Interval Overlap Rule: new.start < existing.end AND new.end > existing.start
    overlap = db.query(Booking).filter(
        Booking.resource_id == resource_id,
        Booking.date == date,
        Booking.status.in_([BookingStatus.UPCOMING, BookingStatus.ONGOING]),
        Booking.start_time < end,
        Booking.end_time > start
    ).first()

    if overlap:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "detail": f"{resource.name} is already booked {overlap.start_time}–{overlap.end_time}, overlapping with requested {start}–{end}",
                "code": "BOOKING_OVERLAP"
            }
        )

    new_booking = Booking(
        resource_id=resource_id,
        user_id=user_id,
        date=date,
        start_time=start,
        end_time=end,
        purpose=purpose,
        status=BookingStatus.UPCOMING
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking