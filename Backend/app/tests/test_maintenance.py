import pytest
import uuid
from fastapi import status
from app.models.user import User
from app.models.asset import Asset
from app.models.maintenance import MaintenanceRequest
from app.utils.enums import Role, AssetStatus, MaintenanceStatus, Priority

def setup_maintenance_fixtures(db):
    employee = User(
        id=uuid.uuid4(),
        name="Priya Shah",
        email="priya@company.com",
        hashed_password="secure_password_hash",
        role=Role.EMPLOYEE,
        is_active=True
    )
    manager = User(
        id=uuid.uuid4(),
        name="Aditi Rao",
        email="aditi@company.com",
        hashed_password="secure_password_hash",
        role=Role.ASSET_MANAGER,
        is_active=True
    )
    asset = Asset(
        id=uuid.uuid4(),
        tag="AF-0062",
        name="Projector",
        status=AssetStatus.AVAILABLE,
        category_id=uuid.uuid4(),
        department_id=uuid.uuid4()
    )
    db.add_all([employee, manager, asset])
    db.commit()
    return employee, manager, asset

# ============================================================================
# 1. MAINTENANCE REQUEST CREATION & ROUTING
# ============================================================================
def test_create_maintenance_request_initializes_as_pending(db_session, client, generate_token):
    """Verifies that newly raised tickets are properly initialized as PENDING[cite: 79]."""
    employee, _, asset = setup_maintenance_fixtures(db_session)
    token = generate_token(employee.id, Role.EMPLOYEE.value)
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "asset_id": str(asset.id),
        "issue_description": "Projector bulb not turning on",
        "priority": Priority.MEDIUM.value
    }

    response = client.post("/api/v1/maintenance/requests", json=payload, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == MaintenanceStatus.PENDING.value
    assert asset.status == AssetStatus.AVAILABLE.value  # Core Rule: Stays available until approval [cite: 122]


# ============================================================================
# 2. STATUS LIFECYCLE STATE MACHINE AUTO-UPDATES
# ============================================================================
def test_maintenance_approval_and_resolution_lifecycle_transitions(db_session, client, generate_token):
    """Validates the state machine transitions: AVAILABLE -> UNDER_MAINTENANCE -> AVAILABLE[cite: 20, 80]."""
    employee, manager, asset = setup_maintenance_fixtures(db_session)
    
    # Establish a baseline pending ticket row in the DB
    ticket = MaintenanceRequest(
        id=uuid.uuid4(),
        asset_id=asset.id,
        requester_id=employee.id,
        issue_description="Flickering lens array",
        status=MaintenanceStatus.PENDING,
        priority=Priority.MEDIUM,
        created_at="2026-07-12T14:00:00Z"
    )
    db_session.add(ticket)
    db_session.commit()

    manager_token = generate_token(manager.id, Role.ASSET_MANAGER.value)
    headers = {"Authorization": f"Bearer {manager_token}"}

    # Step A: Asset Manager approves the request [cite: 79]
    decision_response = client.patch(
        f"/api/v1/maintenance/requests/{ticket.id}/decision",
        json={"decision": "APPROVED"},
        headers=headers
    )
    assert decision_response.status_code == status.HTTP_200_OK
    db_session.refresh(asset)
    assert asset.status == AssetStatus.UNDER_MAINTENANCE  # Auto-updates to maintenance engine state 

    # Step B: Mark the ticket as RESOLVED [cite: 79]
    status_response = client.patch(
        f"/api/v1/maintenance/requests/{ticket.id}/status",
        json={"status": "RESOLVED"},
        headers=headers
    )
    assert status_response.status_code == status.HTTP_200_OK
    db_session.refresh(asset)
    assert asset.status == AssetStatus.AVAILABLE  # Safely returns back to pool