from fastapi import Depends
from sqlalchemy.orm import Session

from app.infra.sqlAlchemy.config.session_sqlAlchemy import get_db
from app.infra.sqlAlchemy.repo.order_repo import (
    OrderRepository
)
from app.usecases.order import (
    OrderService
)


def get_order_repository(
    db: Session = Depends(get_db)
):
    return OrderRepository(db)


def get_order_usecases(
    repo = Depends(get_order_repository)
):
    return OrderService(repo)