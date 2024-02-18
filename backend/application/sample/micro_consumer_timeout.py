import asyncio
from random import randint


async def summer(a, b):
    print("summer started")
    await asyncio.sleep(1)
    print("summer done")
    return a + b


async def multiply(a, b):
    print("multiply started")
    await asyncio.sleep(2)
    print("multiply done")
    return a * b


async def long_process():
    print("long task started")
    await asyncio.sleep(10)
    print("long task done")
    return 1


# it can not be reused! so deleted!
# summer_task = summer(1, 2)
# multiply_task = multiply(1, 2)
# long_process_task = long_process()


async def with_timeout(coroutine, timeout):
    try:
        result = await asyncio.wait_for(coroutine, timeout=timeout)
        print("task result", result)
        return result
    except asyncio.TimeoutError:
        print("timeout")
    except Exception as e:
        print(e)


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(consume_messages())
    loop.run_forever()


async def produce_fake_messages():
    k = randint(0,3)
    tasks = {
        0:  summer(1, 3),
        1:  multiply(1, 2),
        2:  long_process(),
    }
    if k in tasks:
        return tasks[k]
    return None


async def consume_messages():
    while True:
        task = await produce_fake_messages()
        if task:
            await asyncio.gather(with_timeout(task, timeout=5))
        else:
            pass # no messages



if __name__ == '__main__':
    main()
