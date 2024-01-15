

async def create_task(loop, task_func):
    listener_task = loop.create_task(task_func())
    return listener_task
