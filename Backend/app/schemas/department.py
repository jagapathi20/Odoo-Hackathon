from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List
from app.utils.enums import DeptStatus

# Common baseline fields shared across requests and responses
class DepartmentBase(BaseModel):
    name: str = Field(..., max_length=100, example="Engineering")
    parent_department_id: Optional[UUID] = None

# Fields required only when creating a department
class DepartmentCreate(DepartmentBase):
    head_id: Optional[UUID] = None

# Fields available for partial updates
class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    head_id: Optional[UUID] = None
    parent_department_id: Optional[UUID] = None
    status: Optional[DeptStatus] = None

# Nested user footprint placeholder to prevent early circular user imports
class UserMinOut(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True

# Fully validated serialization shape returned by endpoints
class DepartmentOut(DepartmentBase):
    id: UUID
    status: DeptStatus
    head: Optional[UserMinOut] = None

    class Config:
        from_attributes = True

# Standard paginated collection envelope
class DepartmentListOut(BaseModel):
    items: List[DepartmentOut]
    total: int
    page: int
    page_size: int