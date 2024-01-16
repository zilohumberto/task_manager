from math import pi

from application.services.queue.handler import task


@task(task_name="get_pi")
async def get_pi():
    return pi
