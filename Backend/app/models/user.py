import uuid
from sqlalchemy import Column, String, ForeignKey, Enum, text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.enums import Role

class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        server_default=text("gen_random_uuid()")
    )
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    role = Column(
        Enum(Role), 
        nullable=False, 
        default=Role.EMPLOYEE, 
        server_default=Role.EMPLOYEE.value
    )
    
    # Active status toggle (instead of hard-deleting)
    is_active = Column(Boolean, nullable=False, default=True, server_default="true")
    
    department_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("departments.id", ondelete="SET NULL"), 
        nullable=True
    )

    # Relationships
    department = relationship("Department", foreign_keys=[department_id], back_populates="employees")
    managed_department = relationship("Department", foreign_keys="[Department.head_id]", back_populates="head")
    
    # These will link to the upcoming models we build
    allocations = relationship("Allocation", back_populates="holder")
    bookings = relationship("Booking", back_populates="user")
    maintenance_requests = relationship("MaintenanceRequest", back_populates="requester")