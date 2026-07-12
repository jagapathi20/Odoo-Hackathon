from enum import Enum

class Role(str, Enum):
    ADMIN = "ADMIN"
    ASSET_MANAGER = "ASSET_MANAGER"
    DEPARTMENT_HEAD = "DEPARTMENT_HEAD"
    EMPLOYEE = "EMPLOYEE"

class DeptStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class AssetStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    ALLOCATED = "ALLOCATED"
    RESERVED = "RESERVED"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"
    LOST = "LOST"
    RETIRED = "RETIRED"
    DISPOSED = "DISPOSED"

class AllocationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"

class TransferStatus(str, Enum):
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"

class BookingStatus(str, Enum):
    UPCOMING = "UPCOMING"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class MaintenanceStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    TECHNICIAN_ASSIGNED = "TECHNICIAN_ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"

class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class AuditItemResult(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"
    MISSING = "MISSING"
    DAMAGED = "DAMAGED"

class AuditCycleStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"

class NotificationType(str, Enum):
    ALERT = "ALERT"
    APPROVAL = "APPROVAL"
    BOOKING = "BOOKING"

class Condition(str, Enum):
    NEW = "NEW"
    GOOD = "GOOD"
    FAIR = "FAIR"
    POOR = "POOR"
    DAMAGED = "DAMAGED"