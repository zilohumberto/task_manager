import asyncio

from application.services.queue.consumer import consumer


asyncio.run(consumer())
