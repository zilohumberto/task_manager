from functools import partial

from app import task_service, app
from application.services.tasks_definition.tasks import TASK_MAP
from application.models.enums import TaskStatus
from .callbacks import finished_callback


async def consumer():
    with app.app_context():
        queue_tasks = task_service.queue_tasks
        repository = task_service.repository
        task_listeners = []
        while True:
            queued_tasks = queue_tasks.receive()
            for queued_task in queued_tasks:
                task_id = queued_task[0]
                task_queue_handler = queued_task[1]
                print("task getting: ", task_id)
                task_record = repository.get(pk=task_id)
                if task_record is None:
                    continue
                if task_record.name in TASK_MAP:
                    listener = await TASK_MAP[task_record.name](task_id=task_id)
                    repository.mark_running(obj=task_record)
                    listener.add_done_callback(
                        partial(finished_callback, repository=repository)
                    )
                    task_listeners.append(listener)
                    print("running", "LOL!")
                else:
                    repository.mark_failed(obj=task_record)
                    print("Invalid task", task_record.name)

                queue_tasks.delete(task_queue_handler)

            # this loop will keep growing.
            # since Tasks aren't removed from this list.
            # how do you plan to manage this list?

            # also, added the db call repository.get
            for task_listener in task_listeners:
                task = repository.get(pk=task_listener.get_name())
                if task.status == TaskStatus.RUNNING:
                    if task_listener.done():
                        task.mark_done()
                    elif task_service.check_timeout(obj=task):
                        task_listener.cancel()
                        task.mark_cancelled()
