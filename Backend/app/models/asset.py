import uuid
from sqlalchemy import Column, String, ForeignKey, Enum, text, Boolean, Numeric, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.enums import AssetStatus, Condition

class Asset(Base):
    __tablename__ = "assets"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        server_default=text("gen_random_uuid()")
    )
    # Unique tag auto-generated in services (e.g., AF-0001)
    tag = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    serial_number = Column(String(100), unique=True, nullable=True, index=True)
    
    status = Column(
        Enum(AssetStatus), 
        nullable=False, 
        default=AssetStatus.AVAILABLE, 
        server_default=AssetStatus.AVAILABLE.value
    )
    condition = Column(
        Enum(Condition), 
        nullable=False, 
        default=Condition.NEW, 
        server_default=Condition.NEW.value
    )
    
    location = Column(String(255), nullable=True)
    is_bookable = Column(Boolean, nullable=False, default=False, server_default="false")
    
    # Financial/tracking fields
    acquisition_date = Column(String(50), nullable=True)  # Stored as ISO string format
    acquisition_cost = Column(Numeric(12, 2), nullable=True)
    
    # Store dynamic category properties here as key-value JSON
    extra_field_values = Column(JSON, nullable=False, default=dict, server_default="'{}'::jsonb")
    
    # PostgreSQL Array to store photo strings
    photo_urls = Column(ARRAY(String), nullable=False, default=list, server_default="'{}'::varchar[]")

    # Foreign Keys
    category_id = Column(UUID(as_uuid=True), ForeignKey("asset_categories.id", ondelete="PROTECT"), nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    category = relationship("AssetCategory", back_populates="assets")
    department = relationship("Department", back_populates="assets")
    
    allocations = relationship("Allocation", back_populates="asset")
    bookings = relationship("Booking", back_populates="asset")
    maintenance_requests = relationship("MaintenanceRequest", back_populates="asset")
    audit_items = relationship("AuditItem", back_populates="asset")