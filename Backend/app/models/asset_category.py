import uuid
from sqlalchemy import Column, String, JSON, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class AssetCategory(Base):
    __tablename__ = "asset_categories"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        server_default=text("gen_random_uuid()")
    )
    name = Column(String(100), unique=True, nullable=False, index=True)
    
    # Stores dynamic schema configuration, e.g., [{"key": "warranty_period", "label": "Warranty Period", "type": "text"}]
    extra_fields = Column(JSON, nullable=False, default=list, server_default="'[]'::jsonb")

    # Relationships
    assets = relationship("Asset", back_populates="category")