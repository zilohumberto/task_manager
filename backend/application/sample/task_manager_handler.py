import asyncio
import queue
import time
from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime, timedelta
from typing import Optional, Sequence

@dataclass
class Task:
    # uuid4 referenced here is not a type, it is a func. to ref a type
    # use `from uuid import UUID` and then _id: UUID | None
    _id: uuid4 = None  # why are all the values None? what state does none represent?
    instance: asyncio.tasks.Task = None
    name: str = None
    start_time: datetime = None
    end_time: Optional[datetime] = None
    status: str = "created"  # lets use an enum for this.


# lets try to encapsulate any state in a class, and then
# use an instance of that class in code. this helps with dependency
# injection during tests, or replacing this interface with a persistent
# queue at a later point.
new_tasks_queue = queue.Queue()
tasks: Sequence[Task] = []

# config as global is fine.
keep_running_task_manager: bool = True
max_timeout_seconds = 5 * 60  # 5 minutes = 300 seconds


# consider using a different name than `task`
# here you are passing the `task_name` not a `Task` instance.
async def push_task(task):
    # if using asyncio consider using asyncio.Queue instead.
    # here you would do `await new_tasks_queue.put(task)`
    # and the complete setup would be based on coroutines instead.
    new_tasks_queue.put(task)


# consider keeping tasks impls in a separate file.
# and the ability to add task names to reference these functions.
async def x():
    print("XXXXXX")
    await asyncio.sleep(20)
    print("Done XXX")


async def y():
    print("YYYYYY")
    await asyncio.sleep(2)
    print("Done YYYY")


async def get_tasks_status():
    print("-------")
    for task in tasks:
        print("> ", task.name, task._id, task.start_time, task.status)


async def create_task(loop, task_func):
    listener_task = loop.create_task(task_func())
    return listener_task


def hola(value, **kwargs):
    print(value, kwargs)


# this a queue consumer.
async def hear_new_tasks():
    loop = asyncio.get_event_loop()
    # simulate task coming from API!
    # lets move the simulation outside of the `hear_new_tasks`
    await push_task("x")
    await push_task("get_tasks_status")
    await push_task("z")
    await push_task("get_tasks_status")
    await push_task("y")

    while True:
        if not new_tasks_queue.empty():
            # have a look at block and timeout params in the get call.
            new_task = new_tasks_queue.get()

            # why is this map inside the while loop?
            # can this be defined before?
            # can this be defined dynamically?
            task_mp = {
                "x": x,
                "y": y,
                "get_tasks_status": get_tasks_status,
            }
            task_func = task_mp.get(new_task) or None
            if task_func:
                task_instance = await create_task(loop=loop, task_func=task_func)
                task_instance.add_done_callback(hola)
                t = Task(
                        instance=task_instance,
                        name=new_task,
                        start_time=datetime.utcnow(),
                        # can we start tracking the task when it is pushed to the queue
                        # rather than when processing starts ?
                        _id=uuid4(),
                    )

                print(task_instance.done())
                tasks.append(
                    t
                )
                task_instance.set_name(t._id)
            else:
                print("Invalid task", task_func)

        # this loop will keep growing.
        # since Tasks aren't removed from this list.
        # how do you plan to manage this list?
        for task in tasks:
            if task.status == "created":
                # _state - accessing private field of an external lib?
                if task.instance.done() == "FINISHED":
                    print(f"{task.name} started at {task.start_time} is done!")
                    task.end_time = datetime.utcnow()
                    task.status = "finished"
                else:
                    time_difference = datetime.utcnow() - task.start_time
                    if time_difference >= timedelta(seconds=max_timeout_seconds):
                        # force cancel due timeout!
                        task.status = "stopped"
                        task.instance.cancel()

        # can we avoid a sleep here using the `block` param in the `queue.get` method.
        # a sleep results in the system not doing anything if one pass of the loop is
        # past the `empty` check and a new task arrives after that.
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(hear_new_tasks())  # this call need to be non blocking.
    print("HERE SHOULD RUN THE API, but asnyc.run takes the entire loop!!")
