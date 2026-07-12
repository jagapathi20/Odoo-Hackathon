ffrom pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from app.utils.enums import Role

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    department_id: Optional[UUID] = None

class UserOut(BaseModel):
    id: UUID
    name: str
    email: str
    role: Role
    department_id: Optional[UUID] = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

class RoleUpdate(BaseModel):
    role: Role

class UserListOut(BaseModel):
    items: list[UserOut]
    total: int
    page: int
    page_size: int