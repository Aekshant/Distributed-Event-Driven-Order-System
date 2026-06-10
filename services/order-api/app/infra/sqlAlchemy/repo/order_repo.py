
from app.infra.sqlAlchemy.config.session_sqlAlchemy import SessionLocal
from app.infra.sqlAlchemy.repo.main_repo import SqlGenericRepository
from app.infra.sqlAlchemy.model.order_model import OrderModel

user_repo = SqlGenericRepository(SessionLocal, OrderModel)