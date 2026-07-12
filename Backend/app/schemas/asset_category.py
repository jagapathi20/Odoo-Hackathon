from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List, Dict, Any

class ExtraFieldSchema(BaseModel):
    key: str = Field(..., example="warranty_period")
    label: str = Field(..., example="Warranty Period")
    type: str = Field(..., example="text")

class AssetCategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    extra_fields: List[ExtraFieldSchema] = Field(default_factory=list)

class AssetCategoryCreate(AssetCategoryBase):
    pass

class AssetCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    extra_fields: Optional[List[ExtraFieldSchema]] = None

class AssetCategoryOut(AssetCategoryBase):
    id: UUID

    class Config:
        from_attributes = True

class AssetCategoryListOut(BaseModel):
    items: List[AssetCategoryOut]
    total: int
    page: int
    page_size: int