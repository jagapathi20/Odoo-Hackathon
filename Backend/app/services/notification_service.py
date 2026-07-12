from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone

from app.models.notification import Notification
from app.models.activity_log import ActivityLog
from app.utils.enums import NotificationType

def dispatch_notification(
    db: Session, 
    user_id: UUID, 
    notification_type: NotificationType, 
    message: str
) -> Notification:
    """
    Creates and dispatches an internal application notification.
    Feeds frontend tracking tabs via React Query short polling loops.
    """
    current_time = datetime.now(timezone.utc).isoformat()
    db_notification = Notification(
        user_id=user_id,
        type=notification_type,
        message=message,
        is_read=False,
        created_at=current_time
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def log_system_activity(
    db: Session, 
    actor_id: UUID, 
    action: str, 
    target: str
) -> ActivityLog:
    """
    Appends an immutable row entry into the global activity ledger.
    Restricted to administrative operations and system audit trailing.
    """
    current_time = datetime.now(timezone.utc).isoformat()
    db_log = ActivityLog(
        actor_id=actor_id,
        action=action,
        target=target,
        timestamp=current_time
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log