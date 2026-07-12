from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_asset_manager, require_management
from app.models.user import User
from app.models.asset import Asset
from app.models.allocation import Allocation, TransferRequest
from app.schemas.allocation import (
    AllocationCreate, AllocationOut, AllocationReturnRequest,
    TransferRequestCreate, TransferRequestOut, TransferDecision
)
from app.utils.enums import AssetStatus, AllocationStatus, TransferStatus, Role

router = APIRouter(tags=["Allocations & Transfers"])

@router.post("/allocations", response_model=AllocationOut, status_code=status.HTTP_201_CREATED)
def allocate_asset(
    alloc_in: AllocationCreate,
    db: Session = Depends(get_db),
    manager: User = Depends(require_management)
):
    """
    Allocates an asset to a user.
    Enforces the core business rule: returns a 409 conflict with current holder 
    details if the asset is already checked out.
    """
    asset = db.query(Asset).filter(Asset.id == alloc_in.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    # Enforce Department Head boundaries: can only allocate assets within their own department
    if manager.role == Role.DEPARTMENT_HEAD and asset.department_id != manager.department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Department Heads can only allocate assets within their own department."
        )

    # Core Rule: Check if already allocated
    if asset.status == AssetStatus.ALLOCATED:
        active_alloc = db.query(Allocation).filter(
            Allocation.asset_id == asset.id,
            Allocation.status == AllocationStatus.ACTIVE
        ).first()
        
        holder_name = active_alloc.holder.name if (active_alloc and active_alloc.holder) else "Unknown"
        dept_name = active_alloc.holder.department.name if (active_alloc and active_alloc.holder and active_alloc.holder.department) else "Unknown"
        holder_id = active_alloc.holder_id if active_alloc else alloc_in.holder_id
        
        # Structure the 409 shape exactly as requested in the API contract
        conflict_payload = {
            "detail": f"Asset {asset.tag} is currently held by {holder_name} ({dept_name})",
            "code": "ASSET_ALREADY_ALLOCATED",
            "current_holder": {
                "id": holder_id,
                "name": holder_name,
                "department": dept_name
            }
        }
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=conflict_payload)

    # Process successful checkout
    current_time_str = datetime.now(timezone.utc).isoformat()
    db_alloc = Allocation(
        asset_id=asset.id,
        holder_id=alloc_in.holder_id,
        status=AllocationStatus.ACTIVE,
        allocated_on=current_time_str,
        expected_return_date=alloc_in.expected_return_date
    )
    
    asset.status = AssetStatus.ALLOCATED
    db.add(db_alloc)
    db.commit()
    db.refresh(db_alloc)
    return db_alloc

@router.post("/allocations/{id}/return", response_model=AllocationOut)
def return_asset(
    id: UUID,
    return_in: AllocationReturnRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Processes asset returns, logs the equipment's condition, and resets it to AVAILABLE."""
    alloc = db.query(Allocation).filter(Allocation.id == id, Allocation.status == AllocationStatus.ACTIVE).first()
    if not alloc:
        raise HTTPException(status_code=404, detail="Active allocation record not found")
        
    # Employees can only trigger returns for assets currently assigned to them
    if current_user.role == Role.EMPLOYEE and alloc.holder_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only return assets held by you.")

    current_time_str = datetime.now(timezone.utc).isoformat()
    alloc.status = AllocationStatus.RETURNED
    alloc.returned_on = current_time_str
    alloc.condition_on_return = return_in.condition_on_return
    alloc.notes = return_in.notes
    
    # Revert asset status back to the available pool
    alloc.asset.status = AssetStatus.AVAILABLE
    
    db.commit()
    db.refresh(alloc)
    return alloc

@router.post("/allocations/{id}/transfer-request", response_model=TransferRequestOut, status_code=status.HTTP_201_CREATED)
def request_asset_transfer(
    id: UUID,
    transfer_in: TransferRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Initiates an ownership transfer request for an actively allocated asset."""
    alloc = db.query(Allocation).filter(Allocation.id == id, Allocation.status == AllocationStatus.ACTIVE).first()
    if not alloc:
        raise HTTPException(status_code=404, detail="Active allocation record not found")
        
    db_transfer = TransferRequest(
        allocation_id=alloc.id,
        from_holder_id=alloc.holder_id,
        to_holder_id=transfer_in.to_holder_id,
        status=TransferStatus.REQUESTED,
        reason=transfer_in.reason
    )
    db.add(db_transfer)
    db.commit()
    db.refresh(db_transfer)
    return db_transfer

@router.patch("/transfers/{id}/approve", response_model=TransferRequestOut)
def handle_transfer_decision(
    id: UUID,
    decision_in: TransferDecision,
    db: Session = Depends(get_db),
    manager: User = Depends(require_management)
):
    """Approves or rejects an asset transfer request, automatically shifting underlying allocations on approval."""
    transfer = db.query(TransferRequest).filter(TransferRequest.id == id, TransferRequest.status == TransferStatus.REQUESTED).first()
    if not transfer:
        raise HTTPException(status_code=404, detail="Pending transfer request not found")

    if decision_in.decision == TransferStatus.REJECTED:
        transfer.status = TransferStatus.REJECTED
        transfer.rejection_reason = decision_in.rejection_reason
        db.commit()
        db.refresh(transfer)
        return transfer

    # Apply Transfer Approval Cascades
    current_time_str = datetime.now(timezone.utc).isoformat()
    old_alloc = transfer.allocation
    
    # 1. Terminate old allocation record
    old_alloc.status = AllocationStatus.RETURNED
    old_alloc.returned_on = current_time_str
    old_alloc.notes = f"Transferred to user ID: {transfer.to_holder_id}"
    
    # 2. Spawn new allocation record
    new_alloc = Allocation(
        asset_id=old_alloc.asset_id,
        holder_id=transfer.to_holder_id,
        status=AllocationStatus.ACTIVE,
        allocated_on=current_time_str,
        expected_return_date=old_alloc.expected_return_date
    )
    db.add(new_alloc)
    
    # 3. Finalize transfer request state
    transfer.status = TransferStatus.APPROVED
    
    db.commit()
    db.refresh(transfer)
    return transfer

@router.get("/allocations", response_model=List[AllocationOut])
def list_allocations(
    status: Optional[AllocationStatus] = None,
    department_id: Optional[UUID] = None,
    overdue: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lists allocations with optional filters, including a flag for overdue items."""
    query = db.query(Allocation)
    
    if status:
        query = query.filter(Allocation.status == status)
    if department_id:
        query = query.join(User, Allocation.holder_id == User.id).filter(User.department_id == department_id)
    if overdue:
        current_date = datetime.now(timezone.utc).isoformat()[:10]  # Compare YYYY-MM-DD strings
        query = query.filter(
            Allocation.status == AllocationStatus.ACTIVE,
            Allocation.expected_return_date < current_date
        )
        
    return query.all()