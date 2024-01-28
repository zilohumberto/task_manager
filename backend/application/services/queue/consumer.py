from asyncio import sleep
from functools import partial
from typing import Sequence

from app import task_service, app, logging
from application.services.tasks_definition.tasks import TASK_MAP
from application.models.enums import TaskStatus
from application.services.queue.callbacks import finished_callback
from application.services.queue.models import Message, MessageKind
from settings.default import MAX_TIMEOUT_SECONDS


async def consumer():
    with app.app_context():
        queue_tasks = task_service.queue_tasks
        repository = task_service.repository
        listeners = {}
        while True:
            queued_tasks: Sequence[Message] = queue_tasks.receive()

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
                queue_message_done = False
                if task_record.name in TASK_MAP:
                    if task_kind == MessageKind.task:
                        repository.mark_running(obj=task_record)
                        listener = await TASK_MAP[task_record.name](task_id=task_id)
                        listener.add_done_callback(
                            partial(finished_callback, repository=repository)
                        )
                        listeners[task_id] = listener
                        queue_tasks.send(
                            message=Message(
                                body=str(task_id),
                                kind=MessageKind.health_check,
                                delay_seconds=MAX_TIMEOUT_SECONDS,
                            )
                        )
                        logging.info(f"sent health_check for {task_record.name}")
                        queue_message_done = True
                    elif task_kind == MessageKind.health_check:
                        if task_record.status == TaskStatus.RUNNING:
                            task_listener = listeners.get(task_id)
                            if task_listener is None:
                                logging.warning(
                                    f"no listener for tasks {task_kind}:{task_id} - skipping"
                                )
                                repository.mark_failed(obj=task_record)
                                queue_message_done = True
                            else:
                                is_done = task_listener.done()
                                logging.info(
                                    f"Task[{task_record.name}: {task_id}] -> It's done? R: {is_done}"
                                )
                                if is_done:
                                    repository.mark_done(obj=task_record)
                                    queue_message_done = True
                                elif task_service.check_timeout(obj=task_record):
                                    task_listener.cancel()
                                    repository.mark_cancelled(obj=task_record)
                                    queue_message_done = True
                        elif task_record.status != TaskStatus.CREATED:
                            queue_message_done = True
                    else:
                        logging.error(f"task kind '{task_kind}' is not implemented")
                        queue_message_done = True
                else:
                    repository.mark_failed(obj=task_record)
                    logging.info(f"Invalid task {task_record.name}")

                if queue_message_done:
                    # either task or health_check should be deleted!
                    queue_tasks.delete(message=queued_task)
                    # if a health_check task is done with his purpose, the listeners can be deleted
                    if task_kind == MessageKind.health_check and task_id in listeners:
                        del listeners[task_id]

            # currently is needed!
            # somehow the listeners are loosing the track of the task.
            await sleep(0.005)
