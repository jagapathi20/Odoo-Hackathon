import pytest
import uuid
from fastapi import status
from app.models.user import User
from app.models.asset import Asset
from app.models.audit import AuditCycle, AuditItem
from app.utils.enums import Role, AssetStatus, AuditCycleStatus, AuditItemResult

def setup_audit_fixtures(db):
    manager = User(
        id=uuid.uuid4(),
        name="Aditi Rao",
        email="aditi@company.com",
        hashed_password="secure_password_hash",
        role=Role.ASSET_MANAGER,
        is_active=True
    )
    unverified_asset = Asset(
        id=uuid.uuid4(),
        tag="AF-9921",
        name="Corporate Core Router",
        status=AssetStatus.AVAILABLE,
        category_id=uuid.uuid4(),
        department_id=uuid.uuid4()
    )
    db.add_all([manager, unverified_asset])
    db.commit()
    db.refresh(manager)
    db.refresh(unverified_asset)
    return manager, unverified_asset

# ============================================================================
# 1. AUDITOR PRIVILEGE BOUNDARY ENFORCEMENT
# ============================================================================
def test_only_assigned_auditors_can_modify_audit_items(db_session, client, generate_token):
    """Enforces that an operator must be explicitly registered on the cycle."""
    manager, asset = setup_audit_fixtures(db_session)
    unassigned_user = User(
        id=uuid.uuid4(), name="Intruder", email="intruder@company.com",
        hashed_password="pw", role=Role.EMPLOYEE, is_active=True
    )
    db_session.add(unassigned_user)
    db_session.commit()
    
    cycle = AuditCycle(
        id=uuid.uuid4(), name="Q3 Verification", status=AuditCycleStatus.OPEN,
        start_date="2026-07-01", end_date="2026-07-15", auditor_ids=[str(manager.id)]
    )
    db_session.add(cycle)
    db_session.flush()

    item = AuditItem(
        id=uuid.uuid4(), cycle_id=cycle.id, asset_id=asset.id,
        result=AuditItemResult.UNVERIFIED, expected_location="HQ Floor 2"
    )
    db_session.add(item)
    db_session.commit()

    token = generate_token(unassigned_user.id, Role.EMPLOYEE.value)
    headers = {"Authorization": f"Bearer {token}"}

    payload = {"result": "MISSING", "notes": "Test"}

    response = client.patch(f"/api/v1/audits/items/{item.id}", json=payload, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


# ============================================================================
# 2. STATUS TRANSITION CASCADES ON CYCLE CLOSE
# ============================================================================
def test_close_audit_cycle_cascades_missing_items_to_lost_status(db_session, client, generate_token):
    """Validates that confirming an item as MISSING moves it to LOST."""
    manager, asset = setup_audit_fixtures(db_session)
    
    cycle = AuditCycle(
        id=uuid.uuid4(), name="Annual Field Reconciliation", status=AuditCycleStatus.OPEN,
        start_date="2026-07-01", end_date="2026-07-15", auditor_ids=[str(manager.id)]
    )
    db_session.add(cycle)
    db_session.flush()

    item = AuditItem(
        id=uuid.uuid4(), cycle_id=cycle.id, asset_id=asset.id,
        result=AuditItemResult.MISSING, expected_location="HQ Floor 2"
    )
    db_session.add(item)
    db_session.commit()

    token = generate_token(manager.id, Role.ASSET_MANAGER.value)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(f"/api/v1/audits/cycles/{cycle.id}/close", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == AuditCycleStatus.CLOSED.value
    assert response.json()["assets_marked_lost"] == 1

    db_session.refresh(asset)
    assert asset.status == AssetStatus.LOST