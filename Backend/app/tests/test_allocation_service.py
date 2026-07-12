import pytest
import uuid
from app.models.user import User
from app.models.asset import Asset
from app.models.allocation import Allocation
from app.utils.enums import Role, AssetStatus, AllocationStatus
from app.services.allocation_service import check_and_allocate, AllocationConflictError

def test_allocation_service_raises_custom_conflict_exception(db_session):
    """Verifies that the service layer bypasses routers and directly throws structured error payloads."""
    dept_id = uuid.uuid4()
    
    # Register core entities within the database session
    current_holder = User(
        id=uuid.uuid4(), name="Alice Smith", email="alice@corp.com",
        hashed_password="pw", role=Role.EMPLOYEE, department_id=dept_id, is_active=True
    )
    target_employee = User(
        id=uuid.uuid4(), name="Bob Jones", email="bob@corp.com",
        hashed_password="pw", role=Role.EMPLOYEE, department_id=dept_id, is_active=True
    )
    asset = Asset(
        id=uuid.uuid4(), tag="AF-9999", name="Corporate Laptop",
        status=AssetStatus.ALLOCATED, category_id=uuid.uuid4(), department_id=dept_id
    )
    db_session.add_all([current_holder, target_employee, asset])
    db_session.flush()

    # Create active baseline allocation tracking mapping row
    active_alloc = Allocation(
        id=uuid.uuid4(), asset_id=asset.id, holder_id=current_holder.id,
        status=AllocationStatus.ACTIVE, allocated_on="2026-07-01T10:00:00Z"
    )
    db_session.add(active_alloc)
    db_session.commit()

    # Execute service allocation attempt and intercept the specific custom domain exception
    with pytest.raises(AllocationConflictError) as exc_info:
        check_and_allocate(
            db=db_session,
            asset_id=asset.id,
            holder_id=target_employee.id,
            expected_return="2026-08-01"
        )
    
    # Enforce contract rules within the custom exception properties
    error_payload = exc_info.value.current_holder_info
    assert error_payload["code"] == "ASSET_ALREADY_ALLOCATED"
    assert error_payload["current_holder"]["name"] == "Alice Smith"
    assert error_payload["current_holder"]["id"] == current_holder.id