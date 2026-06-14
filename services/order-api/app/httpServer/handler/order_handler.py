
from http import HTTPStatus
import logging
from uuid import UUID

from app.usecases.order_usecases import OrderService
from app.httpServer.common import fail_response, ok_response
from app.domain.orders.order_dto import (
    CreateOrderRequestDTO
)


class OrderHandler:
    def __init__(self, service: OrderService):
        self.service = service
        self.logger = logging.getLogger("uvicorn.error")

    async def create_order(self, request: CreateOrderRequestDTO):
        # try:
            self.logger.info(f"DATA = {request}")
            data = await self.service.create_order(request)
            return ok_response(data, "Success", status_code=HTTPStatus.CREATED)
        # except Exception as e:
        #     return fail_response("Unexpected server error", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    async def get_by_id(self, order_id: UUID):
        try:
            data = await self.service.get_by_id(order_id)
            return ok_response(data, "Success")
        except Exception as e:
            return fail_response("Unexpected server error", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


    async def get_list(self, limit: int | None, page: int | None):
        try:
            offset = ((page - 1) * limit ) if (limit and page) else None

            data = await self.service.get_list(limit, offset)
            return ok_response(data, "Success")
        except Exception as e:
            self.logger.error(e)
            return fail_response("Unexpected server error", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)