from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import JSON
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4, UUID
from sqlalchemy import DateTime

from app.infra.sqlAlchemy.config.Base import Base


class OrderHistoryModel(Base):
    __tablename__ = "order_status_history"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    # No ForeignKey constraint
    order_id: Mapped[UUID]

    status: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )