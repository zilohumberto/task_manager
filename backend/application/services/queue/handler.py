import asyncio


async def create_task(loop, task_func, **kwargs):
    async with asyncio.timeout(5) as cm:
        await task_func(**kwargs)
    return cm


def task(task_name: str):
    def wrapper(func):
        async def async_wrapper(**kwargs):
            task_id = kwargs.pop("task_id")
            loop = asyncio.get_event_loop()
            listener_task = await create_task(loop, func, **kwargs)
            listener_task.set_name(task_id)
            return listener_task
        return async_wrapper

    return wrapper
