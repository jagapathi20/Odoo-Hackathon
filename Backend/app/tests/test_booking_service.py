import pytest
import uuid
from fastapi import HTTPException, status
from app.models.user import User
from app.models.asset import Asset
from app.models.booking import Booking
from app.utils.enums import Role, AssetStatus, BookingStatus
from app.services.booking_service import validate_and_create_booking

def test_booking_service_allows_back_to_back_intervals(db_session):
    """Evaluates standalone booking services to confirm back-to-back edge parameters pass safely."""
    user = User(
        id=uuid.uuid4(), name="Developer Jagapathi", email="jagapathi@corp.com",
        hashed_password="pw", role=Role.EMPLOYEE, is_active=True
    )
    resource = Asset(
        id=uuid.uuid4(), tag="ROOM-01", name="Scrum Room",
        status=AssetStatus.AVAILABLE, category_id=uuid.uuid4(), is_bookable=True
    )
    db_session.add_all([user, resource])
    db_session.commit()

    # Establish initial anchor row: 09:00 - 10:00
    booking_1 = Booking(
        id=uuid.uuid4(), resource_id=resource.id, user_id=user.id,
        date="2026-07-12", start_time="09:00", end_time="10:00",
        status=BookingStatus.UPCOMING
    )
    db_session.add(booking_1)
    db_session.commit()

    # Attempt to book a strict back-to-back follow-up slice: 10:00 - 11:00
    # The rule (new.start < existing.end AND new.end > existing.start) must evaluate to False.
    new_booking = validate_and_create_booking(
        db=db_session,
        resource_id=resource.id,
        user_id=user.id,
        date="2026-07-12",
        start="10:00",
        end="11:00",
        purpose="Backend Engineering Sync"
    )

    assert new_booking.id is not None
    assert new_booking.start_time == "10:00"
    assert new_booking.status == BookingStatus.UPCOMING