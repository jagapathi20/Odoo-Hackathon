import uuid
from sqlalchemy import Column, String, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        server_default=text("gen_random_uuid()")
    )
    
    action = Column(String(100), nullable=False, index=True)  # e.g., "ALLOCATION_CREATED"
    target = Column(String(100), nullable=False)              # e.g., Asset tag "AF-0114"
    timestamp = Column(String(50), nullable=False)           # ISO string timestamp
    
    # User who performed the action
    actor_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    actor = relationship("User")