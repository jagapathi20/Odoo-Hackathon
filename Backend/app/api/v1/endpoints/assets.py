from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_asset_manager
from app.models.user import User
from app.models.asset import Asset
from app.models.asset_category import AssetCategory
from app.models.allocation import Allocation
from app.models.maintenance import MaintenanceRequest
from app.schemas.asset import (
    AssetCreate, AssetUpdate, AssetOut, AssetDetailOut, 
    AssetListOut, AssetStatusOverride, AssetHistoryListOut, HistoryItemOut
)
from app.utils.enums import AssetStatus

router = APIRouter(prefix="/assets", tags=["Assets"])

@router.get("", response_model=AssetListOut)
def list_assets(
    tag: Optional[str] = None,
    serial: Optional[str] = None,
    category_id: Optional[UUID] = None,
    status: Optional[AssetStatus] = None,
    department_id: Optional[UUID] = None,
    location: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lists assets using flexible filters. 
    The 'search' parameter targets tags, serials, and names, fulfilling 
    the baseline text-match QR scoping requirement.
    """
    query = db.query(Asset)
    
    if tag:
        query = query.filter(Asset.tag == tag)
    if serial:
        query = query.filter(Asset.serial_number == serial)
    if category_id:
        query = query.filter(Asset.category_id == category_id)
    if status:
        query = query.filter(Asset.status == status)
    if department_id:
        query = query.filter(Asset.department_id == department_id)
    if location:
        query = query.filter(Asset.location.ilike(f"%{location}%"))
    if search:
        query = query.filter(
            Asset.tag.ilike(f"%{search}%") | 
            Asset.serial_number.ilike(f"%{search}%") | 
            Asset.name.ilike(f"%{search}%")
        )
        
    total = query.count()
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.post("", response_model=AssetOut, status_code=status.HTTP_201_CREATED)
def register_asset(
    asset_in: AssetCreate,
    db: Session = Depends(get_db),
    manager: User = Depends(require_asset_manager)
):
    """
    Registers a new asset into the repository. 
    Auto-calculates the unique Asset Tag tracking sequence server-side.
    """
    category = db.query(AssetCategory).filter(AssetCategory.id == asset_in.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Target asset category not found")
        
    # Sequence generator: Auto-increments total count for clean sequential tags (AF-XXXX)
    asset_count = db.query(Asset).count()
    generated_tag = f"AF-{str(asset_count + 1).zfill(4)}"
    
    db_asset = Asset(
        tag=generated_tag,
        name=asset_in.name,
        serial_number=asset_in.serial_number,
        condition=asset_in.condition,
        location=asset_in.location,
        is_bookable=asset_in.is_bookable,
        acquisition_date=asset_in.acquisition_date,
        acquisition_cost=asset_in.acquisition_cost,
        extra_field_values=asset_in.extra_field_values,
        photo_urls=asset_in.photo_urls,
        category_id=asset_in.category_id,
        status=AssetStatus.AVAILABLE
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.get("/{id}", response_model=AssetDetailOut)
def get_asset_detail(id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetches deep profile information regarding a target asset asset."""
    asset = db.query(Asset).filter(Asset.id == id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset record not found")
        
    # Inject current holder detail if the asset is actively checked out
    current_holder = None
    if asset.status == AssetStatus.ALLOCATED:
        active_alloc = db.query(Allocation).filter(
            Allocation.asset_id == asset.id, 
            Allocation.status == "ACTIVE"
        ).first()
        if active_alloc and active_alloc.holder:
            current_holder = {
                "type": "employee",
                "id": active_alloc.holder.id,
                "name": active_alloc.holder.name
            }
            
    # Cast representation onto detailed output scheme
    asset_detail = AssetDetailOut.from_orm(asset)
    asset_detail.current_holder = current_holder
    return asset_detail

@router.patch("/{id}", response_model=AssetOut)
def edit_asset_core_fields(
    id: UUID,
    asset_in: AssetUpdate,
    db: Session = Depends(get_db),
    manager: User = Depends(require_asset_manager)
):
    """Modifies descriptive metadata variables without touching the business-critical lifecycles."""
    asset = db.query(Asset).filter(Asset.id == id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset record not found")
        
    update_data = asset_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(asset, key, value)
        
    db.commit()
    db.refresh(asset)
    return asset

@router.patch("/{id}/status", response_model=AssetOut)
def override_asset_status(
    id: UUID,
    status_in: AssetStatusOverride,
    db: Session = Depends(get_db),
    manager: User = Depends(require_asset_manager)
):
    """Enforces the strict, server-side terminal lifecycle transitions."""
    asset = db.query(Asset).filter(Asset.id == id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset record not found")
        
    # Restricted transition validator check
    allowed_overrides = [AssetStatus.RETIRED, AssetStatus.DISPOSED, AssetStatus.LOST]
    if status_in.status not in allowed_overrides:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Manual override status must be one of: {[s.value for s in allowed_overrides]}"
        )
        
    asset.status = status_in.status
    db.commit()
    db.refresh(asset)
    return asset

@router.get("/{id}/history", response_model=AssetHistoryListOut)
def get_asset_history(id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Compiles a unified chronological timeline from allocation and maintenance tables."""
    asset = db.query(Asset).filter(Asset.id == id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset record not found")
        
    history_events = []
    
    # 1. Gather all recorded Allocations
    allocations = db.query(Allocation).filter(Allocation.asset_id == id).all()
    for alloc in allocations:
        history_events.append({
            "type": "ALLOCATION",
            "date": alloc.allocated_on,
            "detail": f"Allocated to user {alloc.holder.name if alloc.holder else 'Unknown'}"
        })
        if alloc.returned_on:
            history_events.append({
                "type": "RETURN",
                "date": alloc.returned_on,
                "detail": f"Returned to pool. Condition logged: {alloc.condition_on_return or 'N/A'}"
            })
            
    # 2. Gather all recorded Maintenance Actions
    tickets = db.query(MaintenanceRequest).filter(MaintenanceRequest.asset_id == id).all()
    for ticket in tickets:
        if ticket.resolved_on:
            history_events.append({
                "type": "MAINTENANCE",
                "date": ticket.resolved_on,
                "detail": f"Resolved ticket: {ticket.issue_description[:50]}... by {ticket.technician_name or 'Tech'}"
            })
            
    # Sort events by descending date sequence
    history_events.sort(key=lambda x: x["date"], reverse=True)
    return {"items": history_events}