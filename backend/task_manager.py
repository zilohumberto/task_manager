import asyncio

from service.workers.worker import Worker


if __name__ == '__main__':
    asyncio.run(Worker().start())
