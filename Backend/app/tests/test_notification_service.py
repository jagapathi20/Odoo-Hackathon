import pytest
import uuid
from app.models.notification import Notification
from app.models.activity_log import ActivityLog
from app.utils.enums import NotificationType
from app.services.notification_service import dispatch_notification, log_system_activity

def test_dispatch_notification_creates_unread_record(db_session):
    """Verifies internal app notifications initialize as unread for short-polling consumers."""
    target_user_id = uuid.uuid4()
    
    notification = dispatch_notification(
        db=db_session,
        user_id=target_user_id,
        notification_type=NotificationType.ALERT,
        message="Asset AF-0021 is overdue by 3 days."
    )
    
    assert notification.id is not None
    assert notification.is_read is False
    assert notification.type == NotificationType.ALERT
    assert "overdue" in notification.message

def test_log_system_activity_records_immutable_ledger_row(db_session):
    """Ensures administrative modifications write clean rows into the security audit trail."""
    actor_id = uuid.uuid4()
    
    log_entry = log_system_activity(
        db=db_session,
        actor_id=actor_id,
        action="ROLE_PROMOTED",
        target="USER_UUID_1234"
    )
    
    assert log_entry.id is not None
    assert log_entry.action == "ROLE_PROMOTED"
    assert log_entry.target == "USER_UUID_1234"
    assert log_entry.timestamp is not None