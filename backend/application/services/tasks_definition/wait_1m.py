from asyncio import sleep
from application.services.queue.handler import task


@task(task_name="wait_1m")
async def wait_1m(**kwargs):
    await sleep(60)
