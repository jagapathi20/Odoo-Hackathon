import pytest
import uuid
from fastapi import status
from app.models.user import User
from app.models.asset import Asset
from app.models.allocation import Allocation, TransferRequest
from app.utils.enums import Role, AssetStatus, AllocationStatus, TransferStatus

def create_mock_user(db, name, email, role, department_id=None):
    """Helper to create test users safely."""
    user = User(
        id=uuid.uuid4(),
        name=name,
        email=email,
        hashed_password="mocked_password_hash_123456",
        role=role,
        department_id=department_id or uuid.uuid4(),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_mock_asset(db, name, status_val, department_id, tag="AF-0114"):
    """Helper with safe UUID/serial handling."""
    asset = Asset(
        id=uuid.uuid4(),
        tag=tag,
        name=name,
        serial_number=f"SN-{uuid.uuid4().hex[:8].upper()}",  # Fixed .hex usage
        status=status_val,
        department_id=department_id,
        category_id=uuid.uuid4(),
        is_bookable=False
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

# ============================================================================
# 1. THE 409 CONFLICT STRUCTURAL API CONTRACT TEST
# ============================================================================
def test_allocate_asset_already_allocated_returns_structured_409(db_session, client, generate_token):
    """Ensures double-allocation blocks with the requested API error payload shape."""
    admin_user = create_mock_user(db_session, "Admin Manager", "admin@corp.com", Role.ADMIN)
    holder_user = create_mock_user(db_session, "Priya Shah", "priya@corp.com", Role.EMPLOYEE)
    target_employee = create_mock_user(db_session, "Raj Patel", "raj@corp.com", Role.EMPLOYEE)
    
    allocated_asset = create_mock_asset(db_session, "ThinkPad X1", AssetStatus.ALLOCATED, admin_user.department_id)
    
    # Establish existing active baseline allocation row
    active_alloc = Allocation(
        id=uuid.uuid4(),
        asset_id=allocated_asset.id,
        holder_id=holder_user.id,
        status=AllocationStatus.ACTIVE,
        allocated_on="2026-07-01T00:00:00Z"
    )
    db_session.add(active_alloc)
    db_session.commit()
    
    token = generate_token(admin_user.id, Role.ADMIN.value)
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "asset_id": str(allocated_asset.id),
        "holder_id": str(target_employee.id),
        "expected_return_date": "2026-08-01"
    }
    
    response = client.post("/api/v1/allocations", json=payload, headers=headers)
    
    assert response.status_code == status.HTTP_409_CONFLICT
    error_data = response.json()["detail"]
    assert error_data["code"] == "ASSET_ALREADY_ALLOCATED"
    assert "is currently held by Priya Shah" in error_data["detail"]

# ============================================================================
# 2. THE DEPARTMENT HEAD ISOLATION CROSS-BOUNDARY CHECK
# ============================================================================
def test_department_head_cannot_allocate_outside_their_department(db_session, client, generate_token):
    """Enforces that Department Heads can only manage assets inside their domain boundaries."""
    dept_a = uuid.uuid4()
    dept_b = uuid.uuid4()
    
    dept_head = create_mock_user(db_session, "Head A", "head_a@corp.com", Role.DEPARTMENT_HEAD, department_id=dept_a)
    target_employee = create_mock_user(db_session, "Staff B", "staff_b@corp.com", Role.EMPLOYEE, department_id=dept_b)
    isolated_asset = create_mock_asset(db_session, "MacBook Pro", AssetStatus.AVAILABLE, department_id=dept_b)
    
    token = generate_token(dept_head.id, Role.DEPARTMENT_HEAD.value)
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "asset_id": str(isolated_asset.id),
        "holder_id": str(target_employee.id),
        "expected_return_date": "2026-12-31"
    }
    
    response = client.post("/api/v1/allocations", json=payload, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

# ============================================================================
# 3. TRANSFER APPROVAL CASCADES
# ============================================================================
def test_approve_transfer_request_cascades_allocation_records(db_session, client, generate_token):
    """Validates multi-step atomicity: terminates old allocation and spawns the new holder record."""
    manager = create_mock_user(db_session, "Asset Mgr", "mgr@corp.com", Role.ASSET_MANAGER)
    user_a = create_mock_user(db_session, "User A", "a@corp.com", Role.EMPLOYEE)
    user_b = create_mock_user(db_session, "User B", "b@corp.com", Role.EMPLOYEE)
    
    asset = create_mock_asset(db_session, "iPad Pro", AssetStatus.ALLOCATED, manager.department_id)
    
    old_alloc = Allocation(
        id=uuid.uuid4(), asset_id=asset.id, holder_id=user_a.id,
        status=AllocationStatus.ACTIVE, allocated_on="2026-07-01T00:00:00Z"
    )
    db_session.add(old_alloc)
    db_session.flush()
    
    transfer = TransferRequest(
        id=uuid.uuid4(), allocation_id=old_alloc.id, from_holder_id=user_a.id,
        to_holder_id=user_b.id, status=TransferStatus.REQUESTED, reason="Project switch"
    )
    db_session.add(transfer)
    db_session.commit()
    
    token = generate_token(manager.id, Role.ASSET_MANAGER.value)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.patch(
        f"/api/v1/transfers/{transfer.id}/approve",
        json={"decision": "APPROVED"},
        headers=headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == TransferStatus.APPROVED.value
    
    # Assert database transformations
    db_session.refresh(old_alloc)
    assert old_alloc.status == AllocationStatus.RETURNED
    
    new_alloc = db_session.query(Allocation).filter(
        Allocation.asset_id == asset.id, 
        Allocation.status == AllocationStatus.ACTIVE
    ).first()
    assert new_alloc is not None
    assert new_alloc.holder_id == user_b.id