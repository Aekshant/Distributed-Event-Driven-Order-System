from pydantic import BaseModel, ConfigDict
from datetime import datetime
from dataclasses import dataclass
from uuid import UUID


class CreateOrderHistoryRequestDTO(BaseModel):
    order_id: UUID
    status: str

class OrderHistoryResponseDTO(BaseModel):
    id: UUID
    order_id: UUID
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ResponseDTO(BaseModel):
    status: int
    success: bool
    message: str
    data: OrderHistoryResponseDTO


@dataclass
class OrderHistory:
    id: UUID
    order_id: UUID
    status: str
    created_at: datetime