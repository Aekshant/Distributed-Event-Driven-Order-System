from pydantic import BaseModel, ConfigDict
from datetime import datetime
from dataclasses import dataclass
from uuid import UUID

@dataclass
class Product:
    product_id: UUID
    quantity: int

class ProductDTO(BaseModel):
    product_id: UUID
    quantity: int

class CreateOrderRequestDTO(BaseModel):
    user_id: int
    amount: float
    items: list[ProductDTO]
    payment_method: str

class OrderResponseDTO(BaseModel):
    id: UUID
    user_id: int
    amount: float
    items: list[Product]
    payment_method: str
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
    items: list[ProductDTO]
    payment_method: str
    created_at: datetime