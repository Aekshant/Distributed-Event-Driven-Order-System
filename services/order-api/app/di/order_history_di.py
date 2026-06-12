from fastapi import Depends
from sqlalchemy.orm import Session

from app.infra.sqlAlchemy.config.session_sqlAlchemy import get_db
from app.infra.sqlAlchemy.repo.order_history_repo import (
    OrderHistoryRepository
)
from app.usecases.order_history_usecases import (
    OrderHistoryService
)


def get_order_history_repository(
    db: Session = Depends(get_db)
):
    return OrderHistoryRepository(db)


def get_order_history_usecases(
    repo = Depends(get_order_history_repository)
):
    return OrderHistoryService(repo)



# def get_order_handler(
#     service: OrderService = Depends(get_order_usecases),
# ):
#     return OrderHandler(service)