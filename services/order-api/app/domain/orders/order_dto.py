from pydantic import BaseModel, ConfigDict
from datetime import datetime
from dataclasses import dataclass
from uuid import UUID

class CreateOrderRequestDTO(BaseModel):
    user_id: int
    amount: float

class OrderResponseDTO(BaseModel):
    id: UUID
    user_id: int
    amount: float
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ResponseDTO(BaseModel):
    status: int
    success: bool
    message: str
    data: OrderResponseDTO

@dataclass
class Order:
    id: UUID
    user_id: int
    amount: float
    status: str
    created_at: datetime