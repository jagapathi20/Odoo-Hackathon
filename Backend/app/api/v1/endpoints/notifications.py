from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.notification import Notification
from app.schemas.notification import NotificationListOut, NotificationOut
from app.utils.enums import NotificationType

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=NotificationListOut)
def list_notifications(
    type: Optional[NotificationType] = None,
    read: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Feeds React Query polling components, filtering alerts by type categories."""
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if type:
        query = query.filter(Notification.type == type)
    if read is not None:
        query = query.filter(Notification.is_read == read)
        
    notifications = query.order_by(Notification.created_at.desc()).all()
    unread_count = db.query(Notification).filter(
        Notification.user_id == current_user.id, 
        Notification.is_read == False
    ).count()
    
    return {"items": notifications, "unread_count": unread_count}

@router.patch("/{id}/read", response_model=NotificationOut)
def mark_notification_as_read(id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Flags a specific incoming notification message row as read."""
    notification = db.query(Notification).filter(Notification.id == id, Notification.user_id == current_user.id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification item not found")
        
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification

@router.patch("/read-all")
def mark_all_notifications_as_read(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Bulk-acknowledges all pending user notifications."""
    db.query(Notification).filter(Notification.user_id == current_user.id).update({"is_read": True})
    db.commit()
    return {"detail": "All notifications marked as read."}