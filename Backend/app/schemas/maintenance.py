from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List
from app.utils.enums import MaintenanceStatus, Priority

class MaintenanceRequestBase(BaseModel):
    asset_id: UUID
    issue_description: str = Field(..., max_length=1000)
    priority: Priority = Priority.MEDIUM
    photo_url: Optional[str] = Field(None, max_length=500)

class MaintenanceRequestCreate(MaintenanceRequestBase):
    pass

class MaintenanceDecision(BaseModel):
    decision: MaintenanceStatus  # APPROVED or REJECTED
    rejection_reason: Optional[str] = Field(None, max_length=500)

class TechnicianAssignment(BaseModel):
    technician_name: str = Field(..., max_length=255)

class MaintenanceStatusUpdate(BaseModel):
    status: MaintenanceStatus  # IN_PROGRESS or RESOLVED

class AssetMinOut(BaseModel):
    id: UUID
    tag: str
    name: Optional[str] = None

    class Config:
        from_attributes = True

class MaintenanceRequestOut(BaseModel):
    id: UUID
    status: MaintenanceStatus
    priority: Priority
    issue_description: str
    rejection_reason: Optional[str] = None
    technician_name: Optional[str] = None
    photo_url: Optional[str] = None
    created_at: str
    resolved_on: Optional[str] = None
    asset: AssetMinOut

    class Config:
        from_attributes = True

class MaintenanceListOut(BaseModel):
    items: List[MaintenanceRequestOut]