# kafka/consumer.py

import json
from confluent_kafka import Consumer


class KafkaConsumer:

    def __init__(
        self,
        bootstrap_servers: str,
        group_id: str,
    ):
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest"
        })

    def subscribe(self, topics: list[str]):
        self.consumer.subscribe(topics)

    def poll(self):
        msg = self.consumer.poll(1.0)

        if msg is None:
            return None

        if msg.error():
            raise Exception(msg.error())

        return json.loads(
            msg.value().decode("utf-8")
        )