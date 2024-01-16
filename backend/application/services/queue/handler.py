import asyncio


async def create_task(loop, task_func, **kwargs):
    listener_task = loop.create_task(task_func(**kwargs))
    return listener_task


def task(task_name: str):
    def wrapper(func):
        async def async_wrapper(**kwargs):
            task_id = kwargs.get("task_id")
            loop = asyncio.get_event_loop()
            listener_task = await create_task(loop, func, **kwargs)
            listener_task.set_name(task_id)
            return listener_task
        return async_wrapper

    return wrapper
