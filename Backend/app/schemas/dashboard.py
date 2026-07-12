from pydantic import BaseModel
from uuid import UUID
from typing import List, Dict, Any
from app.schemas.asset import AssetOut
from app.schemas.booking import BookingOut
from app.schemas.maintenance import MaintenanceRequestOut

class DashboardKPIs(BaseModel):
    assets_available: int
    assets_allocated: int
    maintenance_today: int
    active_bookings: int
    pending_transfers: int
    upcoming_returns: int
    overdue_returns: int

class RecentActivityItem(BaseModel):
    type: str  # e.g., "ALLOCATION"
    text: str
    timestamp: str

class RecentActivityList(BaseModel):
    items: List[RecentActivityItem]

class OverdueDashboardData(BaseModel):
    overdue_returns: List[AssetOut]
    overdue_bookings: List[BookingOut]
    overdue_maintenance: List[MaintenanceRequestOut]