import asyncio
from settings.default import MAX_TIMEOUT_SECONDS


async def with_timeout(coroutine, timeout, **kwargs):
    try:
        return asyncio.wait_for(coroutine(**kwargs), timeout=timeout)
    except asyncio.TimeoutError:
        return -1  # defined timeout as -1


def task(task_name: str):
    def wrapper(func):
        async def async_wrapper(**kwargs):
            return with_timeout(coroutine=func, timeout=MAX_TIMEOUT_SECONDS, **kwargs)
        return async_wrapper
    return wrapper
