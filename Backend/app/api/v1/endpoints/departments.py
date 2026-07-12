from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_admin
from app.models.department import Department
from app.models.user import User
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentOut, DepartmentListOut
from app.utils.enums import DeptStatus

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.get("", response_model=DepartmentListOut)
def list_departments(
    status: Optional[DeptStatus] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Returns flat hierarchy lists readable by all authenticated components."""
    query = db.query(Department)
    
    if status:
        query = query.filter(Department.status == status)
    if search:
        query = query.filter(Department.name.ilike(f"%{search}%"))
        
    total = query.count()
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.post("", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(
    dept_in: DepartmentCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Allows Admin roles to register new structural organizational groups."""
    if dept_in.parent_department_id:
        parent = db.query(Department).filter(Department.id == dept_in.parent_department_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent department not found")

    db_dept = Department(
        name=dept_in.name,
        parent_department_id=dept_in.parent_department_id,
        head_id=dept_in.head_id,
        status=DeptStatus.ACTIVE
    )
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept

@router.patch("/{id}", response_model=DepartmentOut)
def update_department(
    id: UUID,
    dept_in: DepartmentUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Applies patch definitions to designated structural departments."""
    dept = db.query(Department).filter(Department.id == id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
        
    update_data = dept_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(dept, key, value)
        
    db.commit()
    db.refresh(dept)
    return dept