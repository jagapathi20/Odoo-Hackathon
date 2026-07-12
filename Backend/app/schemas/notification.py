from pydantic import BaseModel
from uuid import UUID
from typing import List
from app.utils.enums import NotificationType

class NotificationOut(BaseModel):
    id: UUID
    type: NotificationType
    message: str
    is_read: bool
    created_at: str

    class Config:
        from_attributes = True

class NotificationListOut(BaseModel):
    items: List[NotificationOut]
    unread_count: int