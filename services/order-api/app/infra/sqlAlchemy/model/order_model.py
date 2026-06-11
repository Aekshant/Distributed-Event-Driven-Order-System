from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4, UUID

from app.infra.sqlAlchemy.config.Base import Base


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    user_id: Mapped[int]
    amount: Mapped[float]
    status: Mapped[str]
    created_at: Mapped[datetime]