from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List
from app.utils.enums import AuditCycleStatus, AuditItemResult

class AuditCycleCreate(BaseModel):
    name: str = Field(..., max_length=255)
    scope_department_id: UUID
    scope_location: Optional[str] = Field(None, max_length=255)
    start_date: str = Field(..., example="2026-07-01")  # ISO Date String
    end_date: str = Field(..., example="2026-07-15")    # ISO Date String
    auditor_ids: List[UUID]

class AuditItemUpdate(BaseModel):
    result: AuditItemResult
    notes: Optional[str] = Field(None, max_length=500)

class AuditItemOut(BaseModel):
    id: UUID
    result: AuditItemResult
    expected_location: Optional[str] = None
    notes: Optional[str] = None
    verified_at: Optional[str] = None
    asset: AssetMinOut

    class Config:
        from_attributes = True

class AuditorMinOut(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True

class AuditCycleOut(BaseModel):
    id: UUID
    name: str
    status: AuditCycleStatus
    start_date: str
    end_date: str
    scope_location: Optional[str] = None
    scope_department_id: Optional[UUID] = None
    auditor_ids: List[str]
    items: Optional[List[AuditItemOut]] = None

    class Config:
        from_attributes = True

class DiscrepancyReportItem(BaseModel):
    asset_tag: str
    result: AuditItemResult
    notes: Optional[str] = None

class DiscrepancyReportOut(BaseModel):
    cycle_id: UUID
    flagged_count: int
    items: List[DiscrepancyReportItem]

class AuditCycleCloseResponse(BaseModel):
    id: UUID
    status: AuditCycleStatus = AuditCycleStatus.CLOSED
    assets_marked_lost: int