# infrastructure/kafka/producer.py

import json
from aiokafka import AIOKafkaProducer


class KafkaProducerService:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def publish(
        self,
        topic: str,
        message: dict,
        key: str | None = None,
    ):
        if not self.producer:
            raise RuntimeError("Kafka producer not initialized")
        await self.producer.send_and_wait(
            topic,
            value=message,
            key=key.encode() if key else None,
        )

kafka_producer = KafkaProducerService(
    bootstrap_servers="localhost:9092"
)