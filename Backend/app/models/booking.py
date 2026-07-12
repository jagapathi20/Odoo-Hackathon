import uuid
from sqlalchemy import Column, String, ForeignKey, Enum, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.enums import BookingStatus

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        server_default=text("gen_random_uuid()")
    )
    
    status = Column(
        Enum(BookingStatus), 
        nullable=False, 
        default=BookingStatus.UPCOMING, 
        server_default=BookingStatus.UPCOMING.value
    )
    
    # Stored as ISO date component strings (e.g., "2026-07-12") for easy day-grid filtering
    date = Column(String(50), nullable=False, index=True)
    
    # Stored as 24h format HH:MM strings (e.g., "09:30") to simplify string-comparable overlap rules
    start_time = Column(String(10), nullable=False)
    end_time = Column(String(10), nullable=False)
    
    purpose = Column(String(255), nullable=True)

    # Foreign Keys
    resource_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    asset = relationship("Asset", back_populates="bookings")
    user = relationship("User", back_populates="bookings")