from confluent_kafka.admin import (
    AdminClient,
    NewTopic
)


def create_topics():

    admin_client = AdminClient({
        "bootstrap.servers": "localhost:9092"
    })

    topics = [
        NewTopic(
            topic="order.created",
            num_partitions=3,
            replication_factor=1
        )
    ]

    futures = admin_client.create_topics(
        topics
    )

    for topic, future in futures.items():
        try:
            future.result()
            print(
                f"Topic '{topic}' created successfully"
            )
        except Exception as e:
            print(
                f"Failed to create topic '{topic}': {e}"
            )


if __name__ == "__main__":
    create_topics()