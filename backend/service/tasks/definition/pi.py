from math import pi

from service.tasks.resources import task


@task(task_name="get_pi")
async def get_pi(**kwargs):
    return pi
