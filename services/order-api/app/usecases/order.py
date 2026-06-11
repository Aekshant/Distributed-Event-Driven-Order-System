import uuid

from app.infra.sqlAlchemy.model.order_model import OrderModel

from typing import List, Optional
from datetime import datetime
from uuid import UUID
from app.domain.orders.order_dto import CreateOrderRequestDTO, Order
from app.domain.orders.order_dao import OrderDAO  # Your interface


class OrderService:
    def __init__(self, order_dao: OrderDAO):
        self.order_dao = order_dao

    async def create_order(self, order: CreateOrderRequestDTO) -> Order:
        if order.amount <= 0:
            raise ValueError("An order amount must be greater than zero.")
        order_data = Order(
            id = uuid.uuid4(),
            user_id=order.user_id,
            amount=order.amount,
            status="PENDING",
            created_at=datetime.utcnow()
        )
        return await self.order_dao.create(order_data)

    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        return await self.order_dao.get_by_id(order_id)