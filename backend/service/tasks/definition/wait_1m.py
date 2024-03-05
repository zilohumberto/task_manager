from asyncio import sleep
from service.tasks.resources import task


@task(task_name="wait_1m")
async def wait_1m(**kwargs):
    await sleep(60)
