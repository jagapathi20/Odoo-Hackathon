import uuid
from sqlalchemy import Column, String, ForeignKey, Enum, text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.enums import NotificationType

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        server_default=text("gen_random_uuid()")
    )
    
    type = Column(
        Enum(NotificationType), 
        nullable=False, 
        index=True
    )
    message = Column(String(500), nullable=False)
    is_read = Column(Boolean, nullable=False, default=False, server_default="false")
    created_at = Column(String(50), nullable=False)  # ISO string timestamp
    
    # Recipient of the notification
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    user = relationship("User")