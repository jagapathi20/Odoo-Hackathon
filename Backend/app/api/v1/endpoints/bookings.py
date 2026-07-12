from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.asset import Asset
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingOut, BookingGridResponse, BookingReschedule
from app.utils.enums import AssetStatus, BookingStatus, Role

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.get("", response_model=BookingGridResponse)
def get_booking_slots(
    resource_id: UUID,
    date: str = Query(..., example="2026-07-12"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns a single-resource day/slot grid view for a specific date.
    Calculates fixed intervals and maps active bookings to populate the frontend grid.
    """
    resource = db.query(Asset).filter(Asset.id == resource_id, Asset.is_bookable == True).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Bookable resource not found")

    # Fetch all active bookings for this specific resource and date
    active_bookings = db.query(Booking).filter(
        Booking.resource_id == resource_id,
        Booking.date == date,
        Booking.status.in_([BookingStatus.UPCOMING, BookingStatus.ONGOING])
    ).all()

    # Generate standard hourly slots from 09:00 to 17:00 for the hackathon MVP day-grid
    slots_config = [
        ("09:00", "10:00"), ("10:00", "11:00"), ("11:00", "12:00"),
        ("12:00", "13:00"), ("13:00", "14:00"), ("14:00", "15:00"),
        ("15:00", "16:00"), ("16:00", "17:00")
    ]
    
    computed_slots = []
    for start, end in slots_config:
        booked_by = None
        slot_status = "FREE"
        
        # Check if any active booking overlaps with this slot window
        for b in active_bookings:
            if b.start_time < end and b.end_time > start:
                slot_status = "BOOKED"
                booked_by = b.user.name if b.user else "Team Member"
                break
                
        computed_slots.append({
            "start": start,
            "end": end,
            "status": slot_status,
            "booked_by": booked_by
        })

    return {
        "resource": {"id": resource.id, "name": resource.name},
        "date": date,
        "slots": computed_slots
    }

@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Creates a new resource booking.
    Enforces the strict overlap protection rule before writing to the database.
    """
    resource = db.query(Asset).filter(Asset.id == booking_in.resource_id, Asset.is_bookable == True).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found or is not bookable")

    # Overlap logic implementation: (new.start < existing.end) AND (new.end > existing.start)
    overlapping_booking = db.query(Booking).filter(
        Booking.resource_id == booking_in.resource_id,
        Booking.date == booking_in.date,
        Booking.status.in_([BookingStatus.UPCOMING, BookingStatus.ONGOING]),
        Booking.start_time < booking_in.end_time,
        Booking.end_time > booking_in.start_time
    ).first()

    if overlapping_booking:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "detail": f"{resource.name} is already booked {overlapping_booking.start_time}–{overlapping_booking.end_time}, which overlaps with requested {booking_in.start_time}–{booking_in.end_time}",
                "code": "BOOKING_OVERLAP"
            }
        )

    db_booking = Booking(
        resource_id=booking_in.resource_id,
        user_id=current_user.id,
        date=booking_in.date,
        start_time=booking_in.start_time,
        end_time=booking_in.end_time,
        purpose=booking_in.purpose,
        status=BookingStatus.UPCOMING
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.patch("/{id}/cancel", response_model=BookingOut)
def cancel_booking(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancels a scheduled booking slot. Restricts cancellation to the owner or management."""
    booking = db.query(Booking).filter(Booking.id == id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking record not found")

    if booking.user_id != current_user.id and current_user.role not in [Role.ADMIN, Role.DEPARTMENT_HEAD]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this booking."
        )

    booking.status = BookingStatus.CANCELLED
    db.commit()
    db.refresh(booking)
    return booking