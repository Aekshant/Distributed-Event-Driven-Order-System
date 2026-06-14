from fastapi import Depends
from sqlalchemy.orm import Session

from app.infra.sqlAlchemy.config.session_sqlAlchemy import get_db
from app.di.order_history_di import get_order_history_usecases
from app.di.kafka_di import get_kafka_producer
from app.infra.sqlAlchemy.repo.order_repo import (
    OrderRepository
)
from app.usecases.order_usecases import (
    OrderService
)


def get_order_repository(
    db: Session = Depends(get_db)
):
    return OrderRepository(db)


def get_order_usecases(
    repo = Depends(get_order_repository),
    order_history_repo = Depends(get_order_history_usecases),
    kafka_producer=Depends(get_kafka_producer),
):
    return OrderService(repo, order_history_repo, kafka_producer)