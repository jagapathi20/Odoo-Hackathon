from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional, List
from app.utils.enums import Role

class UserBase(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    department_id: UUID

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    department_id: Optional[UUID] = None
    is_active: Optional[bool] = None

class RoleUpdate(BaseModel):
    role: Role

# Nested target shape for department payloads inside user responses
class DeptMinOut(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True

class UserOut(UserBase):
    id: UUID
    role: Role
    is_active: bool = Field(..., serialization_alias="status") 
    department: Optional[DeptMinOut] = None

    class Config:
        from_attributes = True
        # Ensures that boolean 'is_active' maps smoothly to the 'status' text field in contract
        populate_by_name = True 

class UserListOut(BaseModel):
    items: List[UserOut]
    total: int
    page: int
    page_size: int