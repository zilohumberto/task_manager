from time import sleep
from application.services.queue.handler import task


@task(task_name="wait_5s")
async def wait_5s(**kwargs):
    sleep(5)
