from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional

class ActorMinOut(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True

class ActivityLogOut(BaseModel):
    id: UUID
    action: str
    target: str
    timestamp: str
    actor: Optional[ActorMinOut] = None

    class Config:
        from_attributes = True

class ActivityLogListOut(BaseModel):
    items: List[ActivityLogOut]
    total: int
    page: int
    page_size: int