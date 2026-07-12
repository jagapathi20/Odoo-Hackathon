from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone
from fastapi import HTTPException, status

from app.models.asset import Asset
from app.models.allocation import Allocation
from app.utils.enums import AssetStatus, AllocationStatus

class AllocationConflictError(Exception):
    """Custom exception raised when an asset is already checked out."""
    def __init__(self, current_holder_info: dict):
        self.current_holder_info = current_holder_info

def check_and_allocate(db: Session, asset_id: UUID, holder_id: UUID, expected_return: str = None) -> Allocation:
    """
    Validates asset availability and applies the checkout state transitions.
    Raises an AllocationConflictError if the asset is currently allocated.
    """
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    # Business Rule: Enforce exclusive allocation conflict check
    if asset.status == AssetStatus.ALLOCATED:
        active_alloc = db.query(Allocation).filter(
            Allocation.asset_id == asset.id,
            Allocation.status == AllocationStatus.ACTIVE
        ).first()
        
        holder_name = active_alloc.holder.name if (active_alloc and active_alloc.holder) else "Unknown"
        dept_name = active_alloc.holder.department.name if (active_alloc and active_alloc.holder and active_alloc.holder.department) else "Unknown"
        h_id = active_alloc.holder_id if active_alloc else holder_id
        
        raise AllocationConflictError({
            "detail": f"Asset {asset.tag} is currently held by {holder_name} ({dept_name})",
            "code": "ASSET_ALREADY_ALLOCATED",
            "current_holder": {
                "id": h_id,
                "name": holder_name,
                "department": dept_name
            }
        })

    current_time = datetime.now(timezone.utc).isoformat()
    new_alloc = Allocation(
        asset_id=asset.id,
        holder_id=holder_id,
        status=AllocationStatus.ACTIVE,
        allocated_on=current_time,
        expected_return_date=expected_return
    )
    
    # Update lifecycle state[cite: 1, 2]
    asset.status = AssetStatus.ALLOCATED
    db.add(new_alloc)
    db.commit()
    db.refresh(new_alloc)
    return new_alloc