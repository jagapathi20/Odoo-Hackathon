import uuid
from sqlalchemy import Column, String, ForeignKey, Enum, text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.enums import AllocationStatus, TransferStatus

class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        server_default=text("gen_random_uuid()")
    )
    
    status = Column(
        Enum(AllocationStatus), 
        nullable=False, 
        default=AllocationStatus.ACTIVE, 
        server_default=AllocationStatus.ACTIVE.value
    )
    
    # Timestamps for history & dashboard metrics
    allocated_on = Column(String(50), nullable=False) # ISO String format
    expected_return_date = Column(String(50), nullable=True) # For overdue logic
    returned_on = Column(String(50), nullable=True)
    
    condition_on_return = Column(String(50), nullable=True)
    notes = Column(String(500), nullable=True)

    # Foreign Keys
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    
    # The current holder is a User (Employee/Manager)
    holder_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="PROTECT"), nullable=False)

    # Relationships
    asset = relationship("Asset", back_populates="allocations")
    holder = relationship("User", back_populates="allocations")
    transfer_requests = relationship("TransferRequest", back_populates="allocation")


class TransferRequest(Base):
    __tablename__ = "transfer_requests"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        server_default=text("gen_random_uuid()")
    )
    
    status = Column(
        Enum(TransferStatus), 
        nullable=False, 
        default=TransferStatus.REQUESTED, 
        server_default=TransferStatus.REQUESTED.value
    )
    
    reason = Column(String(500), nullable=True)
    rejection_reason = Column(String(500), nullable=True)
    
    # Foreign Keys
    allocation_id = Column(UUID(as_uuid=True), ForeignKey("allocations.id", ondelete="CASCADE"), nullable=False)
    from_holder_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="PROTECT"), nullable=False)
    to_holder_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="PROTECT"), nullable=False)

    # Relationships
    allocation = relationship("Allocation", back_populates="transfer_requests")
    from_holder = relationship("User", foreign_keys=[from_holder_id])
    to_holder = relationship("User", foreign_keys=[to_holder_id])