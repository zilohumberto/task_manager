from asyncio import sleep
from service.tasks.resources import task
from app import logging

@task(task_name="wait_1m")
async def wait_1m(**kwargs):
    await sleep(60)
    logging.info("Finished wait_1m task")
