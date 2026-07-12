from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List
from app.utils.enums import AllocationStatus, TransferStatus

class AllocationBase(BaseModel):
    asset_id: UUID
    expected_return_date: Optional[str] = None  # ISO format date string

class AllocationCreate(AllocationBase):
    holder_id: UUID

class AllocationReturnRequest(BaseModel):
    condition_on_return: str = Field(..., example="GOOD")
    notes: Optional[str] = Field(None, max_length=500)

class AllocationOut(BaseModel):
    id: UUID
    asset_id: UUID
    status: AllocationStatus
    allocated_on: str
    expected_return_date: Optional[str] = None
    returned_on: Optional[str] = None

    class Config:
        from_attributes = True

# Struct returned upon a 409 Conflict rejection block
class AllocationConflictDetail(BaseModel):
    id: UUID
    name: str
    department: str

class AllocationConflictResponse(BaseModel):
    detail: str
    code: str = "ASSET_ALREADY_ALLOCATED"
    current_holder: AllocationConflictDetail

# --- Transfer Workflow Schemas ---

class TransferRequestCreate(BaseModel):
    to_holder_id: UUID
    reason: Optional[str] = Field(None, max_length=500)

class TransferDecision(BaseModel):
    decision: TransferStatus  # APPROVED or REJECTED
    rejection_reason: Optional[str] = Field(None, max_length=500)

class TransferRequestOut(BaseModel):
    id: UUID
    allocation_id: UUID
    from_holder_id: UUID
    to_holder_id: UUID
    status: TransferStatus
    reason: Optional[str] = None
    rejection_reason: Optional[str] = None

    class Config:
        from_attributes = True