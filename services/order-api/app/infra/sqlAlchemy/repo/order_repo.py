from sqlalchemy.orm import Session
from uuid import UUID

from app.domain.orders.order_dao import OrderDAO
from app.domain.orders.order_dto import Order
from app.infra.sqlAlchemy.model.order_model import OrderModel


class OrderRepository(OrderDAO):
    def __init__(self, db: Session):
        self.db = db


    async def create(self, order: Order) -> Order:

        db_order = OrderModel(
            user_id=order.user_id,
            amount=order.amount,
            status=order.status,
            created_at=order.created_at
        )

        self.db.add(db_order)
        await self.db.commit()
        await self.db.refresh(db_order)

        return self._to_entity(db_order)


    async def get_by_id(self, order_id: UUID) -> Order | None:

        order = await self.db.get(OrderModel, order_id)

        if not order:
            return None

        return self._to_entity(order)


    def update(self, order: Order) -> Order:

        db_order = self.db.get(OrderModel, order.id)

        db_order.amount = order.amount
        db_order.status = order.status

        self.db.commit()
        self.db.refresh(db_order)

        return self._to_entity(db_order)


    def delete(self, order_id: UUID):
        order = self.db.get(OrderModel, order_id)

        if order:
            self.db.delete(order)
            self.db.commit()


    def _to_entity(self, model: OrderModel) -> Order:

        return Order(
            id=model.id,
            user_id=model.user_id,
            amount=model.amount,
            status=model.status,
            created_at=model.created_at
        )