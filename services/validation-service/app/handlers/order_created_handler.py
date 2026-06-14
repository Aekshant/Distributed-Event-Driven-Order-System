# handlers/order_created_handler.py

from app.schemas.order_events import OrderCreatedEvent


class OrderCreatedHandler:

    async def handle(
        self,
        event: OrderCreatedEvent
    ):
        print(
            f"Processing order {event.order_id}"
        )

        # process payment
        # create shipment
        # send email