from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    amount: Mapped[float]
    status: Mapped[str]
    created_at: Mapped[datetime]