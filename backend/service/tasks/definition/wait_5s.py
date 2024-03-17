from asyncio import sleep
from service.tasks.resources import task


@task(task_name="wait_5s")
async def wait_5s(**kwargs):
    await sleep(5)
