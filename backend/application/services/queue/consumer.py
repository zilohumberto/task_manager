from asyncio import gather
from typing import Sequence

from app import task_service, app, logging
from application.services.tasks_definition.tasks import TASK_MAP
from application.services.queue.models import Message, MessageKind


async def consumer():
    with app.app_context():
        queue_tasks = task_service.queue_tasks
        repository = task_service.repository
        while True:
            queued_tasks: Sequence[Message] = queue_tasks.receive()
            coroutines = []
            for queued_task in queued_tasks:
                task_id = queued_task.body
                task_kind = queued_task.kind
                task_record = repository.get(pk=task_id)
                if task_record is None:
                    logging.warning(f"Record not found: {task_id}")
                    continue

                logging.info(
                    f"task getting[{task_kind}]: {task_record.name} [{task_record.status.name}]-> {task_id}"
                )
                # check if task is done with his purpose of live, it not can not be deleted
                if task_record.name in TASK_MAP:
                    if task_kind == MessageKind.task:
                        repository.mark_running(obj=task_record)
                        coroutine = await TASK_MAP[task_record.name](task_id=task_id)
                        coroutines.append(coroutine)
                    else:
                        logging.error(f"task kind '{task_kind}' is not implemented")
                        repository.mark_cancelled(obj=task_record)
                else:
                    repository.mark_failed(obj=task_record)
                    logging.error(f"Invalid task {task_record.name}")
                    repository.mark_cancelled(obj=task_record)

                queue_tasks.delete(message=queued_task)
            if coroutines:
                results = await gather(*coroutines)
                logging.info(f"all results {results}")
                for task_result, queued_task in zip(results, queued_tasks):
                    if task_result == -1:
                        repository.mark_failed(pk=queued_task.body)
                    else:
                        repository.mark_done(pk=queued_task.body)
