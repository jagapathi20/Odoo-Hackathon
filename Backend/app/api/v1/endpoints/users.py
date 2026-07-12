from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_admin, require_management
from app.models.user import User
from app.models.department import Department
from app.schemas.user import UserOut, UserListOut, UserUpdate, RoleUpdate
from app.utils.enums import Role

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=UserListOut)
def list_users(
    department_id: Optional[UUID] = None,
    role: Optional[Role] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management)
):
    """
    Returns the employee directory. Scoped to ADMIN, ASSET_MANAGER, 
    and DEPARTMENT_HEAD for picking targets or managing workflows.
    """
    query = db.query(User)
    
    if department_id:
        query = query.filter(User.department_id == department_id)
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    if search:
        query = query.filter(User.name.ilike(f"%{search}%") | User.email.ilike(f"%{search}%"))
        
    total = query.count()
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.patch("/{id}/role", response_model=UserOut)
def update_user_role(
    id: UUID,
    role_in: RoleUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """The absolute structural boundary preventing self-assigned roles."""
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.role = role_in.role
    db.commit()
    db.refresh(user)
    return user

@router.patch("/{id}", response_model=UserOut)
def update_user(
    id: UUID,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Allows an Admin to modify standard user records or flag them as INACTIVE."""
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    update_data = user_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
        
    db.commit()
    db.refresh(user)
    return user