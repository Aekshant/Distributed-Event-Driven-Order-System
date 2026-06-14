# consumers/order_consumer.py

from app.kafka.consumer import KafkaConsumer
from app.schemas.order_events import OrderCreatedEvent
from app.handlers.order_created_handler import (
    OrderCreatedHandler
)

topic = ["order.created"]
class OrderConsumer:

    def __init__(self):
        self.consumer = KafkaConsumer(
            bootstrap_servers="localhost:9092",
            group_id="payment-service"
        )

        self.handler = OrderCreatedHandler()

    async def start(self):

        self.consumer.subscribe(
            topic
        )

        while True:

            payload = self.consumer.poll()

            if payload is None:
                continue

            print(payload)

            event = OrderCreatedEvent(
                **payload
            )

            await self.handler.handle(
                event
            )