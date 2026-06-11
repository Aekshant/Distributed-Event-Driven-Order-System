from fastapi import APIRouter, Depends
from uuid import UUID

from app.httpServer.handler.order_handler import OrderHandler
from app.di.oder_di import get_order_usecases
from app.domain.orders.order_dto import (
    CreateOrderRequestDTO,
    ResponseDTO
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.get("/{order_id}"
    "",
)
async def get_order(
    order_id: UUID,
    handler: OrderHandler = Depends(get_order_usecases)
):
    return await handler.get_by_id(order_id)

@router.post(
    "",
)
async def create_order(
    request: CreateOrderRequestDTO,
    handler: OrderHandler = Depends(get_order_usecases)
):
    return await handler.create_order(request)