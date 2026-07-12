import pytest
import uuid
from fastapi import status
from app.models.user import User
from app.models.asset import Asset
from app.models.booking import Booking
from app.utils.enums import Role, AssetStatus, BookingStatus

def create_booking_fixtures(db):
    user = User(
        id=uuid.uuid4(),
        name="Arjun Nair",
        email="arjun@company.com",
        hashed_password="hashed_password_123",
        role=Role.EMPLOYEE,
        is_active=True
    )
    resource = Asset(
        id=uuid.uuid4(),
        tag="AF-0062",
        name="Conference Room B2",
        status=AssetStatus.AVAILABLE,
        category_id=uuid.uuid4(),
        is_bookable=True
    )
    db.add_all([user, resource])
    db.commit()
    return user, resource

# ============================================================================
# 1. TIME-SLOT OVERLAP PROTECTION MATRIX
# ============================================================================
@pytest.mark.parametrize(
    "existing_start, existing_end, new_start, new_end, should_conflict",
    [
        ("09:00", "10:00", "09:30", "10:30", True),   # Interior partial collision [cite: 70, 71]
        ("09:00", "10:00", "08:30", "09:30", True),   # Leading partial collision
        ("09:00", "12:00", "10:00", "11:00", True),   # Encompassed nesting collision
        ("09:00", "10:00", "10:00", "11:00", False),  # Back-to-back handoff (Allowed) [cite: 71, 72]
        ("09:00", "10:00", "13:00", "14:00", False),  # Disjoint interval window
    ]
)
def test_booking_overlap_validation_matrix(
    db_session, client, generate_token, 
    existing_start, existing_end, new_start, new_end, should_conflict
):
    """Enforces mathematical boundary handling for resource scheduling combinations."""
    user, resource = create_booking_fixtures(db_session)
    token = generate_token(user.id, Role.EMPLOYEE.value)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Commit the anchor slot to the DB [cite: 70, 71]
    base_booking = Booking(
        id=uuid.uuid4(),
        resource_id=resource.id,
        user_id=user.id,
        date="2026-07-12",
        start_time=existing_start,
        end_time=existing_end,
        status=BookingStatus.UPCOMING
    )
    db_session.add(base_booking)
    db_session.commit()

    payload = {
        "resource_id": str(resource.id),
        "date": "2026-07-12",
        "start_time": new_start,
        "end_time": new_end,
        "purpose": "Product Architecture Evaluation Sync"
    }

    response = client.post("/api/v1/bookings", json=payload, headers=headers)

    if should_conflict:
        assert response.status_code == status.HTTP_409_CONFLICT
        error = response.json()["detail"]
        assert error["code"] == "BOOKING_OVERLAP"
    else:
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["status"] == BookingStatus.UPCOMING.value


# ============================================================================
# 2. DAY-GRID SLOT VIEW RENDERING
# ============================================================================
def test_get_booking_slots_calculates_correct_free_vs_booked_states(db_session, client, generate_token):
    """Ensures the day-view slot mapping correctly reflects booked intervals."""
    user, resource = create_booking_fixtures(db_session)
    token = generate_token(user.id, Role.EMPLOYEE.value)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Inject an active booking reservation row for 09:00 to 10:00 [cite: 70, 71]
    active_booking = Booking(
        id=uuid.uuid4(), resource_id=resource.id, user_id=user.id,
        date="2026-07-12", start_time="09:00", end_time="10:00",
        status=BookingStatus.UPCOMING
    )
    db_session.add(active_booking)
    db_session.commit()

    response = client.get(
        f"/api/v1/bookings?resource_id={resource.id}&date=2026-07-12",
        headers=headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    slots = response.json()["slots"]
    
    # Assert that 09:00 - 10:00 is mapped as BOOKED
    assert slots[0]["start"] == "09:00"
    assert slots[0]["status"] == "BOOKED"
    assert slots[0]["booked_by"] == "Arjun Nair"
    
    # Assert that the subsequent interval is FREE [cite: 71, 72]
    assert slots[1]["start"] == "10:00"
    assert slots[1]["status"] == "FREE"