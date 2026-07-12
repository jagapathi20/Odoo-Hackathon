import uuid
from sqlalchemy import Column, String, ForeignKey, Enum, text
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.enums import AuditCycleStatus, AuditItemResult

class AuditCycle(Base):
    __tablename__ = "audit_cycles"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        server_default=text("gen_random_uuid()")
    )
    name = Column(String(255), nullable=False)
    status = Column(
        Enum(AuditCycleStatus), 
        nullable=False, 
        default=AuditCycleStatus.OPEN, 
        server_default=AuditCycleStatus.OPEN.value
    )
    
    start_date = Column(String(50), nullable=False)  # ISO string format
    end_date = Column(String(50), nullable=False)    # ISO string format
    
    # Store IDs of assigned auditors as a Postgres array of UUID strings
    auditor_ids = Column(ARRAY(String), nullable=False, default=list, server_default="'{}'::varchar[]")
    
    scope_department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    scope_location = Column(String(255), nullable=True)

    # Relationships
    department = relationship("Department")
    items = relationship("AuditItem", back_populates="cycle", cascade="all, delete-orphan")


class AuditItem(Base):
    __tablename__ = "audit_items"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        server_default=text("gen_random_uuid()")
    )
    
    result = Column(
        Enum(AuditItemResult), 
        nullable=False, 
        default=AuditItemResult.UNVERIFIED, 
        server_default=AuditItemResult.UNVERIFIED.value
    )
    
    expected_location = Column(String(255), nullable=True)
    notes = Column(String(500), nullable=True)
    verified_at = Column(String(50), nullable=True)  # Timestamp set upon verification

    # Foreign Keys
    cycle_id = Column(UUID(as_uuid=True), ForeignKey("audit_cycles.id", ondelete="CASCADE"), nullable=False)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    cycle = relationship("AuditCycle", back_populates="items")
    asset = relationship("Asset", back_populates="audit_items")