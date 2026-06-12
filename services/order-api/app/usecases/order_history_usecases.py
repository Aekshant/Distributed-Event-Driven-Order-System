import uuid

from app.infra.sqlAlchemy.model.order_model import OrderModel

from typing import List, Optional
from datetime import datetime
from uuid import UUID
from app.domain.orders_history.order_history_dto import CreateOrderHistoryRequestDTO, OrderHistory
from app.domain.orders_history.order_history_dao import OrderHistoryDAO  # Your interface


class OrderHistoryService:
    def __init__(self, order_history_dao: OrderHistoryDAO):
        self.order_history_dao = order_history_dao

    async def create_order(self, order: CreateOrderHistoryRequestDTO) -> OrderHistory:
        order_data = OrderHistory(
            id = uuid.uuid4(),
            order_id=order.order_id,
            status=order.status,
            created_at=datetime.utcnow()
        )
        return await self.order_history_dao.create(order_data)

    async def get_by_id(self, order_id: UUID) -> Optional[OrderHistory]:
        return await self.order_history_dao.get_by_id(order_id)

    async def get_list(self, limit : int | None, offset : int | None) -> list[OrderHistory]:
        data = await self.order_history_dao.get_list(limit, offset)
        return data