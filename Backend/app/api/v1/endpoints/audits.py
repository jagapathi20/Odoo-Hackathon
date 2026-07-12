from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_asset_manager
from app.models.user import User
from app.models.asset import Asset
from app.models.audit import AuditCycle, AuditItem
from app.schemas.audit import (
    AuditCycleCreate, AuditCycleOut, AuditItemUpdate, AuditItemOut,
    DiscrepancyReportOut, AuditCycleCloseResponse
)
from app.utils.enums import AuditCycleStatus, AuditItemResult, AssetStatus

router = APIRouter(prefix="/audits", tags=["Audits"])

@router.post("/cycles", response_model=AuditCycleOut, status_code=status.HTTP_201_CREATED)
def create_audit_cycle(
    cycle_in: AuditCycleCreate,
    db: Session = Depends(get_db),
    manager: User = Depends(require_asset_manager)
):
    """
    Spawns a new organizational audit cycle.
    Automatically snapshots all active assets matching the scope criteria into audit line items.
    """
    db_cycle = AuditCycle(
        name=cycle_in.name,
        scope_department_id=cycle_in.scope_department_id,
        scope_location=cycle_in.scope_location,
        start_date=cycle_in.start_date,
        end_date=cycle_in.end_date,
        auditor_ids=[str(a_id) for a_id in cycle_in.auditor_ids],
        status=AuditCycleStatus.OPEN
    )
    db.add(db_cycle)
    db.flush()  # Extract the generated cycle ID prior to committing

    # Gather matching inventory items currently flagged inside the target department scope
    asset_scope = db.query(Asset).filter(Asset.department_id == cycle_in.scope_department_id)
    if cycle_in.scope_location:
        asset_scope = asset_scope.filter(Asset.location.ilike(f"%{cycle_in.scope_location}%"))
        
    in_scope_assets = asset_scope.all()

    # Generate explicit baseline unverified snapshot tracking rows for each target asset
    for asset in in_scope_assets:
        db_item = AuditItem(
            cycle_id=db_cycle.id,
            asset_id=asset.id,
            expected_location=asset.location,
            result=AuditItemResult.UNVERIFIED
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_cycle)
    return db_cycle

@router.get("/cycles/{id}", response_model=AuditCycleOut)
def get_audit_cycle_details(id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetches details of an explicit audit cycle including its nested tracking rows."""
    cycle = db.query(AuditCycle).filter(AuditCycle.id == id).first()
    if not cycle:
        raise HTTPException(status_code=404, detail="Audit cycle not found")
    return cycle

@router.patch("/items/{id}", response_model=AuditItemOut)
def update_audit_item_result(
    id: UUID,
    item_in: AuditItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Logs physical verification discoveries. 
    Restricted entirely to the assigned auditors registered on the cycle.
    """
    item = db.query(AuditItem).filter(AuditItem.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Audit item row not found")

    if item.cycle.status == AuditCycleStatus.CLOSED:
        raise HTTPException(status_code=400, detail="Cannot modify items within a closed audit cycle")

    # Enforce contract restriction: current operator must be in the snapshot's auditor list
    if str(current_user.id) not in item.cycle.auditor_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You are not registered as an authorized auditor for this cycle."
        )

    current_time_str = datetime.now(timezone.utc).isoformat()
    item.result = item_in.result
    item.notes = item_in.notes
    item.verified_at = current_time_str

    db.commit()
    db.refresh(item)
    return item

@router.get("/cycles/{id}/discrepancy-report", response_model=DiscrepancyReportOut)
def get_cycle_discrepancy_report(id: UUID, db: Session = Depends(get_db), manager: User = Depends(require_asset_manager)):
    """Auto-computes anomaly vectors where items are explicitly flagged as MISSING or DAMAGED."""
    cycle = db.query(AuditCycle).filter(AuditCycle.id == id).first()
    if not cycle:
        raise HTTPException(status_code=404, detail="Audit cycle not found")

    flagged_items = db.query(AuditItem).filter(
        AuditItem.cycle_id == id,
        AuditItem.result.in_([AuditItemResult.MISSING, AuditItemResult.DAMAGED])
    ).all()

    report_items = [
        {"asset_tag": item.asset.tag, "result": item.result, "notes": item.notes}
        for item in flagged_items if item.asset
    ]

    return {
        "cycle_id": cycle.id,
        "flagged_count": len(report_items),
        "items": report_items
    }

@router.post("/cycles/{id}/close", response_model=AuditCycleCloseResponse)
def close_audit_cycle(
    id: UUID,
    db: Session = Depends(get_db),
    manager: User = Depends(require_asset_manager)
):
    """
    Locks down an active audit cycle to prevent further modifications.
    Cascades status updates, moving assets flagged as MISSING into a global LOST state.
    """
    cycle = db.query(AuditCycle).filter(AuditCycle.id == id, AuditCycle.status == AuditCycleStatus.OPEN).first()
    if not cycle:
        raise HTTPException(status_code=404, detail="Open audit cycle record not found")

    cycle.status = AuditCycleStatus.CLOSED
    
    # Identify items registered as missing during the cycle duration
    missing_items = db.query(AuditItem).filter(
        AuditItem.cycle_id == id,
        AuditItem.result == AuditItemResult.MISSING
    ).all()

    # Apply the server-side status cascade update
    lost_counter = 0
    for item in missing_items:
        if item.asset and item.asset.status != AssetStatus.LOST:
            item.asset.status = AssetStatus.LOST
            lost_counter += 1

    db.commit()
    return {
        "id": cycle.id,
        "status": cycle.status,
        "assets_marked_lost": lost_counter
    }