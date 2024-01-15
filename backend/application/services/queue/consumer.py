import asyncio
import queue
from uuid import uuid4
from datetime import datetime

from backend.application.services.tasks_definition.tasks import TASK_MAP
from backend.application.models.enums import TaskStatus
from backend.application.models.models import Task
from .callbacks import finished_callback
from .handler import create_task


async def consumer():
    loop = asyncio.get_event_loop()
    tasks = []
    # lets try to encapsulate any state in a class, and then
    # use an instance of that class in code. this helps with dependency
    # injection during tests, or replacing this interface with a persistent
    # queue at a later point.
    queue_tasks = queue.Queue()  # TBD: define the queue
    while True:
        if queue_tasks.empty():
            pass
        else:
            task_name = queue_tasks.get()
            if task_name in TASK_MAP:
                task_func = TASK_MAP.get(task_name)
                listener_task = await create_task(loop=loop, task_func=task_func)
                task_obj = Task(
                    listener=listener_task,
                    name=task_name,
                    start_time=datetime.utcnow(),
                    _id=uuid4()
                )
                task_obj.set_name()
                listener_task.add_done_callback(finished_callback)
                tasks.append(task_obj)
            else:
                # Consider send alert!!
                # TBD
                print("Invalid task", task_name)

        # this loop will keep growing.
        # since Tasks aren't removed from this list.
        # how do you plan to manage this list?
        for task in tasks:
            if task.status == TaskStatus.CREATED:
                if task.listener.done():
                    task.mark_done()
                else:
                    if task.check_timeout():
                        task.mark_cancelled()

        # can we avoid a sleep here using the `block` param in the `queue.get` method.
        # a sleep results in the system not doing anything if one pass of the loop is
        # past the `empty` check and a new task arrives after that.
        await asyncio.sleep(0.1)
