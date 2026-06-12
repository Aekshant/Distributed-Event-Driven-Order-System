from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from app.domain.orders_history.order_history_dao import OrderHistoryDAO
from app.domain.orders_history.order_history_dto import OrderHistory
from app.infra.sqlAlchemy.model.order_history_model import OrderHistoryModel


class OrderHistoryRepository(OrderHistoryDAO):
    def __init__(self, db: Session):
        self.db = db


    async def create(self, order: OrderHistory) -> OrderHistory:

        db_order = OrderHistoryModel(
            order_id=order.order_id,
            status=order.status,
            created_at=order.created_at
        )

        self.db.add(db_order)
        await self.db.commit()
        await self.db.refresh(db_order)

        return self._to_entity(db_order)


    async def get_by_id(self, order_history_id: UUID) -> OrderHistory | None:

        data = await self.db.get(OrderHistoryModel, order_history_id)

        if not data:
            return None

        return self._to_entity(data)

    async def get_list(self, limit: int | None, offset: int | None) -> list[OrderHistory]:
        stmt = (
            select(OrderHistoryModel)
            .offset(offset)
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]


    def update(self, order: OrderHistory) -> OrderHistory:

        db_order = self.db.get(OrderHistory, order.id)
        self.db.commit()
        self.db.refresh(db_order)

        return self._to_entity(db_order)


    def delete(self, order_id: UUID):
        order = self.db.get(OrderHistory, order_id)

        if order:
            self.db.delete(order)
            self.db.commit()


    def _to_entity(self, model: OrderHistory) -> OrderHistory:

        return OrderHistory(
            id=model.id,
            order_id=model.order_id,
            status=model.status,
            created_at=model.created_at
        )