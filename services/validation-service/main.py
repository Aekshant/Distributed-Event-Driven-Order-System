# main.py

import asyncio

from app.consumers.order_consumer import (
    OrderConsumer
)


async def main():
    consumer = OrderConsumer()
    await consumer.start()


if __name__ == "__main__":
    asyncio.run(main())