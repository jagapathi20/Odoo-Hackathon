from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID
from typing import Optional, List, Dict, Any
from decimal import Decimal
from app.utils.enums import AssetStatus, Condition
from app.schemas.asset_category import AssetCategoryOut

class AssetBase(BaseModel):
    name: str = Field(..., max_length=255)
    serial_number: Optional[str] = Field(None, max_length=100)
    condition: Condition = Condition.NEW
    location: Optional[str] = Field(None, max_length=255)
    is_bookable: bool = False
    acquisition_date: Optional[str] = None
    acquisition_cost: Optional[Decimal] = None
    extra_field_values: Dict[str, Any] = Field(default_factory=dict)
    photo_urls: List[str] = Field(default_factory=list)

# The client does not supply a 'tag' or 'status' during initial registration
class AssetCreate(AssetBase):
    category_id: UUID

class AssetUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    serial_number: Optional[str] = Field(None, max_length=100)
    condition: Optional[Condition] = None
    location: Optional[str] = Field(None, max_length=255)
    is_bookable: Optional[bool] = None
    acquisition_date: Optional[str] = None
    acquisition_cost: Optional[Decimal] = None
    extra_field_values: Optional[Dict[str, Any]] = None
    photo_urls: Optional[List[str]] = None
    department_id: Optional[UUID] = None

class AssetStatusOverride(BaseModel):
    status: AssetStatus
    reason: str = Field(..., max_length=255)

# A minimal holder representation to prevent circular imports for User profiles
class HolderMinOut(BaseModel):
    type: str = "employee"
    id: UUID
    name: str

class AssetOut(AssetBase):
    id: UUID
    tag: str
    status: AssetStatus
    department_id: Optional[UUID] = None
    category: AssetCategoryOut

    class Config:
        from_attributes = True

# Extended schema that provides detail on who currently has the item checked out
class AssetDetailOut(AssetOut):
    current_holder: Optional[HolderMinOut] = None

class AssetListOut(BaseModel):
    items: List[AssetOut]
    total: int
    page: int
    page_size: int

# Timeline structures mapping to historical feeds
class HistoryItemOut(BaseModel):
    type: str  # ALLOCATION, RETURN, MAINTENANCE
    date: str
    detail: str
    
class AssetHistoryListOut(BaseModel):
    items: List[HistoryItemOut]