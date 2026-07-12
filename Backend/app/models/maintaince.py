import uuid
from sqlalchemy import Column, String, ForeignKey, Enum, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.enums import MaintenanceStatus, Priority

class MaintenanceRequest(Base):
    __tablename__ = "maintenance_requests"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        server_default=text("gen_random_uuid()")
    )
    
    status = Column(
        Enum(MaintenanceStatus), 
        nullable=False, 
        default=MaintenanceStatus.PENDING, 
        server_default=MaintenanceStatus.PENDING.value
    )
    priority = Column(
        Enum(Priority), 
        nullable=False, 
        default=Priority.MEDIUM, 
        server_default=Priority.MEDIUM.value
    )
    
    issue_description = Column(String(1000), nullable=False)
    rejection_reason = Column(String(500), nullable=True)
    technician_name = Column(String(255), nullable=True)
    photo_url = Column(String(500), nullable=True)
    
    # Timestamps for metrics and recent activity feeds
    created_at = Column(String(50), nullable=False)  # ISO string format
    resolved_on = Column(String(50), nullable=True)

    # Foreign Keys
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    requester_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="PROTECT"), nullable=False)

    # Relationships
    asset = relationship("Asset", back_populates="maintenance_requests")
    requester = relationship("User", back_populates="maintenance_requests")