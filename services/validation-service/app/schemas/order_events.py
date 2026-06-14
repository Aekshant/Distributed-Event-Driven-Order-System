from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class OrderCreatedEvent(BaseModel):
    order_id: UUID
    event_type: str
    created_at: datetime
    occurred_at: datetime