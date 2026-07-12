from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_admin
from app.models.user import User
from app.models.asset_category import AssetCategory
from app.schemas.asset_category import AssetCategoryCreate, AssetCategoryUpdate, AssetCategoryOut, AssetCategoryListOut

router = APIRouter(prefix="/categories", tags=["Asset Categories"])

@router.get("", response_model=AssetCategoryListOut)
def list_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Returns all available categories. Open to all authenticated users for dropdown configuration."""
    categories = db.query(AssetCategory).all()
    return {
        "items": categories,
        "total": len(categories),
        "page": 1,
        "page_size": len(categories) if categories else 20
    }

@router.post("", response_model=AssetCategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    cat_in: AssetCategoryCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Registers a unique asset category complete with structured dynamic JSON schema fields."""
    existing = db.query(AssetCategory).filter(AssetCategory.name == cat_in.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category name already exists")
        
    db_cat = AssetCategory(
        name=cat_in.name,
        extra_fields=[field.dict() for field in cat_in.extra_fields]
    )
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

@router.patch("/{id}", response_model=AssetCategoryOut)
def update_category(
    id: UUID,
    cat_in: AssetCategoryUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Partially modifies category descriptions or internal dynamic configurations."""
    cat = db.query(AssetCategory).filter(AssetCategory.id == id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
        
    update_data = cat_in.dict(exclude_unset=True)
    if "extra_fields" in update_data and update_data["extra_fields"] is not None:
        cat.extra_fields = [field.dict() for field in update_data["extra_fields"]]
        del update_data["extra_fields"]
        
    for key, value in update_data.items():
        setattr(cat, key, value)
        
    db.commit()
    db.refresh(cat)
    return cat