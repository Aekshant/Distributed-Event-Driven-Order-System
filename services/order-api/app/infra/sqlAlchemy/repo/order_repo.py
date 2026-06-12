from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from app.domain.orders.order_dao import OrderDAO
from app.domain.orders.order_dto import Order, ProductDTO
from app.infra.sqlAlchemy.model.order_model import OrderModel


class OrderRepository(OrderDAO):
    def __init__(self, db: Session):
        self.db = db


    async def create(self, order: Order) -> Order:

        db_order = OrderModel(
            user_id=order.user_id,
            amount=order.amount,
            items=[
                {
                    "product_id": str(item.product_id),
                    "quantity": item.quantity
                }
                for item in order.items
            ],
            payment_method=order.payment_method,
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

    async def get_list(self, limit: int | None, offset: int | None) -> list[Order]:
        stmt = (
            select(OrderModel)
            .offset(offset)
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]


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
            payment_method=model.payment_method,
            items=[
                ProductDTO(
                    product_id=UUID(item["product_id"]),
                    quantity=item["quantity"]
                )
                for item in model.items
            ],
            created_at=model.created_at
        )