from abc import ABC, abstractmethod
from app.domain.orders.order_dto import Order
from uuid import UUID


class OrderDAO(ABC):

    @abstractmethod
    async def create(self, order: Order) -> Order:
        pass


    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Order | None:
        pass


    @abstractmethod
    async def update(self, order: Order) -> Order:
        pass


    @abstractmethod
    async def delete(self, order_id: UUID) -> None:
        pass