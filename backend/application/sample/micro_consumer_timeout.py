import asyncio
from random import randint


async def summer(a=1, b=2):
    print("summer started")
    await asyncio.sleep(5)
    print("summer done")
    return a + b


async def multiply(a=1, b=2):
    print("multiply started")
    await asyncio.sleep(10)
    print("multiply done")
    return a * b


async def long_process():
    print("long task started")
    await asyncio.sleep(20)
    print("long task done")
    return 1


# it can not be reused! so deleted!
# summer_task = summer(1, 2)
# multiply_task = multiply(1, 2)
# long_process_task = long_process()


async def with_timeout(coroutine, timeout):
    try:
        result = await asyncio.wait_for(coroutine(), timeout=timeout)
        print("task result", result)
        return result
    except asyncio.TimeoutError:
        print("timeout")
    except Exception as e:
        print(e)


def main():
    asyncio.run(consume_messages())


def produce_fake_messages():
    k = randint(0,3)
    tasks = {
        0:  summer,
        1:  multiply,
        2:  long_process,
    }
    if k in tasks:
        return tasks[k]
    return None


async def create_task(loop, task_func, **kwargs):
    listener_task = loop.create_task(task_func(**kwargs))
    return listener_task


async def consume_messages():
    while True:
        task = produce_fake_messages()
        if task:
            r = await asyncio.gather(with_timeout(task, timeout=10))
            print(r, "result ->>>")
        else:
            pass # no messages


if __name__ == '__main__':
    main()