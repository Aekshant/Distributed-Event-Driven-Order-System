from abc import ABC, abstractmethod
from app.domain.orders_history.order_history_dto import OrderHistory
from uuid import UUID


class OrderHistoryDAO(ABC):
    @abstractmethod
    async def create(self, order_history: OrderHistory) -> OrderHistory:
        pass

    @abstractmethod
    async def get_by_id(self, order_history_id: UUID) -> OrderHistory | None:
        pass

    @abstractmethod
    async def get_list(self, limit : int | None, offset : int | None) -> list[OrderHistory]:
        pass

    @abstractmethod
    async def update(self, order: OrderHistory) -> OrderHistory:
        pass

    @abstractmethod
    async def delete(self, order_id: UUID) -> None:
        pass