import uuid
from sqlalchemy import Column, String, ForeignKey, Enum, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.enums import DeptStatus

class Department(Base):
    __tablename__ = "departments"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        server_default=text("gen_random_uuid()")
    )
    name = Column(String(100), nullable=False, index=True)
    status = Column(
        Enum(DeptStatus), 
        nullable=False, 
        default=DeptStatus.ACTIVE, 
        server_default=DeptStatus.ACTIVE.value
    )
    
    # Self-referential hierarchy: a department can belong to a parent department
    parent_department_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("departments.id", ondelete="SET NULL"), 
        nullable=True
    )
    
    # The Department Head points to a record in the users table
    head_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="SET NULL"), 
        nullable=True
    )

    # Relationships
    parent = relationship("Department", remote_side=[id], backref="sub_departments")
    head = relationship("User", foreign_keys=[head_id], back_populates="managed_department")
    employees = relationship("User", foreign_keys="[User.department_id]", back_populates="department")
    assets = relationship("Asset", back_populates="department")