import uuid

from fastapi import Depends
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from app.di.order_history_di import get_order_history_usecases
from app.usecases.order_history_usecases import OrderHistoryService
from app.domain.orders.order_dto import CreateOrderRequestDTO, Order
from app.domain.orders_history.order_history_dto import CreateOrderHistoryRequestDTO, OrderHistory
from app.domain.orders.order_dao import OrderDAO  # Your interface


class OrderService:
    def __init__(
            self,
            order_dao: OrderDAO,
            order_history_service: OrderHistoryService
    ):
        self.order_dao = order_dao
        self.order_history_service = order_history_service


    async def create_order(
            self,
            order: CreateOrderRequestDTO
    ) -> Order:
        if order.amount <= 0:
            raise ValueError("An order amount must be greater than zero.")

        order_data = Order(
            id = uuid.uuid4(),
            user_id=order.user_id,
            amount=order.amount,
            items=order.items,
            payment_method=order.payment_method,
            created_at=datetime.utcnow()
        )
        order_db_data = await self.order_dao.create(order_data)
        order_status = CreateOrderHistoryRequestDTO(
            order_id=order_db_data.id,
            status="PENDING"
        )
        await self.order_history_service.create_order(order_status)
        return order_db_data

    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        return await self.order_dao.get_by_id(order_id)

    async def get_list(self, limit : int | None, offset : int | None) -> list[Order]:
        data = await self.order_dao.get_list(limit, offset)
        print(data)
        return data