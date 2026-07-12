from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.asset import Asset
from app.models.allocation import Allocation
from app.models.booking import Booking
from app.models.maintenance import MaintenanceRequest
from app.models.notification import Notification
from app.schemas.dashboard import DashboardKPIs, RecentActivityList, OverdueDashboardData
from app.utils.enums import AssetStatus, AllocationStatus, BookingStatus, MaintenanceStatus, Role

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/kpis", response_model=DashboardKPIs)
def get_dashboard_kpis(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Returns high-level KPI card counters.
    Enforces server-side scoping: Employees see department metrics, admins/managers see everything.
    """
    asset_q = db.query(Asset)
    alloc_q = db.query(Allocation).filter(Allocation.status == AllocationStatus.ACTIVE)
    maint_q = db.query(MaintenanceRequest)
    book_q = db.query(Booking).filter(Booking.status.in_([BookingStatus.UPCOMING, BookingStatus.ONGOING]))

    # Role-based scoping rule
    if current_user.role == Role.EMPLOYEE:
        asset_q = asset_q.filter(Asset.department_id == current_user.department_id)
        alloc_q = alloc_q.join(User, Allocation.holder_id == User.id).filter(User.department_id == current_user.department_id)
        maint_q = maint_q.filter(MaintenanceRequest.requester_id == current_user.id)
        book_q = book_q.filter(Booking.user_id == current_user.id)

    current_date = datetime.now(timezone.utc).isoformat()[:10]
    
    return {
        "assets_available": asset_q.filter(Asset.status == AssetStatus.AVAILABLE).count(),
        "assets_allocated": asset_q.filter(Asset.status == AssetStatus.ALLOCATED).count(),
        "maintenance_today": maint_q.filter(MaintenanceRequest.status == MaintenanceStatus.IN_PROGRESS).count(),
        "active_bookings": book_q.count(),
        "pending_transfers": 0,  # Extensible stub for tracking workflows
        "upcoming_returns": alloc_q.filter(Allocation.expected_return_date >= current_date).count(),
        "overdue_returns": alloc_q.filter(Allocation.expected_return_date < current_date).count()
    }

@router.get("/recent-activity", response_model=RecentActivityList)
def get_recent_activity(limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetches a recent window of activity events to populate the layout dashboard feed."""
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    raw_logs = query.order_by(Notification.created_at.desc()).limit(limit).all()
    
    activity_items = [
        {"type": log.type.value, "text": log.message, "timestamp": log.created_at}
        for log in raw_logs
    ]
    return {"items": activity_items}