from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_asset_manager
from app.models.user import User
from app.models.asset import Asset
from app.models.maintenance import MaintenanceRequest
from app.schemas.maintenance import (
    MaintenanceRequestCreate, MaintenanceRequestOut, MaintenanceListOut,
    MaintenanceDecision, TechnicianAssignment, MaintenanceStatusUpdate
)
from app.utils.enums import MaintenanceStatus, AssetStatus, Priority

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

@router.post("/requests", response_model=MaintenanceRequestOut, status_code=status.HTTP_201_CREATED)
def create_maintenance_request(
    request_in: MaintenanceRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Creates a new maintenance ticket for an asset. 
    Can be raised by any active user associated with the item.
    """
    asset = db.query(Asset).filter(Asset.id == request_in.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Target asset record not found")

    current_time_str = datetime.now(timezone.utc).isoformat()
    db_request = MaintenanceRequest(
        asset_id=request_in.asset_id,
        requester_id=current_user.id,
        issue_description=request_in.issue_description,
        priority=request_in.priority,
        photo_url=request_in.photo_url,
        status=MaintenanceStatus.PENDING,
        created_at=current_time_str
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.get("/requests", response_model=MaintenanceListOut)
def list_maintenance_requests(
    status: Optional[MaintenanceStatus] = None,
    priority: Optional[Priority] = None,
    asset_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fetches maintenance tickets based on status, priority, or specific assets. 
    The client fetches this dataset flat and splits it out into the Kanban grid columns.
    """
    query = db.query(MaintenanceRequest)
    
    if status:
        query = query.filter(MaintenanceRequest.status == status)
    if priority:
        query = query.filter(MaintenanceRequest.priority == priority)
    if asset_id:
        query = query.filter(MaintenanceRequest.asset_id == asset_id)
        
    return {"items": query.all()}

@router.custom_route("PATCH", "/requests/{id}/decision", response_model=MaintenanceRequestOut)
def handle_maintenance_decision(
    id: UUID,
    decision_in: MaintenanceDecision,
    db: Session = Depends(get_db),
    manager: User = Depends(require_asset_manager)
):
    """
    Allows the Asset Manager to approve or reject a ticket.
    Approving automatically shifts the asset state to UNDER_MAINTENANCE.
    """
    ticket = db.query(MaintenanceRequest).filter(
        MaintenanceRequest.id == id, 
        MaintenanceRequest.status == MaintenanceStatus.PENDING
    ).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Pending maintenance ticket not found")

    if decision_in.decision == MaintenanceStatus.REJECTED:
        ticket.status = MaintenanceStatus.REJECTED
        ticket.rejection_reason = decision_in.rejection_reason
    elif decision_in.decision == MaintenanceStatus.APPROVED:
        ticket.status = MaintenanceStatus.APPROVED
        # Enforce server-side asset state transition rule
        ticket.asset.status = AssetStatus.UNDER_MAINTENANCE
    else:
        raise HTTPException(status_code=400, detail="Invalid decision parameters provided")

    db.commit()
    db.refresh(ticket)
    return ticket

@router.custom_route("PATCH", "/requests/{id}/assign-technician", response_model=MaintenanceRequestOut)
def assign_technician(
    id: UUID,
    assignment_in: TechnicianAssignment,
    db: Session = Depends(get_db),
    manager: User = Depends(require_asset_manager)
):
    """Assigns an explicit service technician name and pushes the state to TECHNICIAN_ASSIGNED."""
    ticket = db.query(MaintenanceRequest).filter(
        MaintenanceRequest.id == id,
        MaintenanceRequest.status == MaintenanceStatus.APPROVED
    ).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Approved maintenance ticket not found")

    ticket.technician_name = assignment_in.technician_name
    ticket.status = MaintenanceStatus.TECHNICIAN_ASSIGNED
    
    db.commit()
    db.refresh(ticket)
    return ticket

@router.custom_route("PATCH", "/requests/{id}/status", response_model=MaintenanceRequestOut)
def update_maintenance_status(
    id: UUID,
    status_in: MaintenanceStatusUpdate,
    db: Session = Depends(get_db),
    manager: User = Depends(require_asset_manager)
):
    """
    Drives work item state tracking (IN_PROGRESS / RESOLVED).
    Resolving a request logs timestamps and returns the underlying asset back to AVAILABLE.
    """
    ticket = db.query(MaintenanceRequest).filter(
        MaintenanceRequest.id == id
    ).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Maintenance ticket not found")

    valid_statuses = [MaintenanceStatus.IN_PROGRESS, MaintenanceStatus.RESOLVED]
    if status_in.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Status updates must map to IN_PROGRESS or RESOLVED")

    ticket.status = status_in.status

    if status_in.status == MaintenanceStatus.RESOLVED:
        current_time_str = datetime.now(timezone.utc).isoformat()
        ticket.resolved_on = current_time_str
        # Revert the core asset lifecycle marker back to the inventory pool
        ticket.asset.status = AssetStatus.AVAILABLE

    db.commit()
    db.refresh(ticket)
    return ticket