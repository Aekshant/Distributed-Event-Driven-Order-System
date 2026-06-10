from app.infra.sqlAlchemy.model.order_model import OrderModel


def createData(data: dict) -> OrderModel:
    order = OrderModel()