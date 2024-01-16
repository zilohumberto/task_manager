import asyncio
from functools import partial

from application.services.tasks_definition.tasks import TASK_MAP
from application.models.enums import TaskStatus
from .callbacks import finished_callback


async def consumer(repository, queue_tasks):
    task_listeners = []
    while True:
        print("looping queuesdssdsd")
        if queue_tasks.empty():
            pass
        else:
            task_id = queue_tasks.get()
            print("task getting: ", task_id)
            task_record = repository.get(pk=task_id)
            if task_record is None:
                continue
            if task_record.name in TASK_MAP:
                # listener = await TASK_MAP[task_record.name](task_id=task_id)
                repository.mark_running(obj=task_record)
                # listener.add_done_callback(
                #     partial(finished_callback, repository=repository)
                # )
                # task_listeners.append(listener)
                print("running", "LOL!")
            else:
                repository.mark_failed(obj=task_record)
                print("Invalid task", task_record.name)

        # this loop will keep growing.
        # since Tasks aren't removed from this list.
        # how do you plan to manage this list?

        # also, added the db call repository.get
        for task_listener in task_listeners:
            task = repository.get(pk=task_listener.name)
            if task.status == TaskStatus.RUNNING:
                if task_listener.done():
                    task.mark_done()
                elif task.check_timeout():
                    task_listener.cancel()
                    task.mark_cancelled()

        # can we avoid a sleep here using the `block` param in the `queue.get` method.
        # a sleep results in the system not doing anything if one pass of the loop is
        # past the `empty` check and a new task arrives after that.
        await asyncio.sleep(1)
