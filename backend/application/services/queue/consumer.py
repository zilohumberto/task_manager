import asyncio
from asyncio import sleep
from functools import partial
from typing import Sequence

from app import task_service, app, logging
from application.services.tasks_definition.tasks import TASK_MAP
from application.models.enums import TaskStatus
from application.services.queue.callbacks import finished_callback
from application.services.queue.models import Message
from settings.default import MAX_TIMEOUT_SECONDS


def do_check_task_status(task_id, task_record, task_listener, repository):
    if task_record.status == TaskStatus.RUNNING:
        if task_listener is None:
            logging.warning(f"no listener for tasks {task_id} - skipping")
            repository.mark_failed(obj=task_record)
        else:
            is_done = task_listener.done()
            logging.info(
                f"Task[{task_record.name}: {task_id}] -> It's done? R: {is_done}"
            )
            if is_done:
                repository.mark_done(obj=task_record)
            elif task_service.check_timeout(obj=task_record):
                task_listener.cancel()
                repository.mark_cancelled(obj=task_record)


def clear_listeners():
    """
    if task_id in listeners:
        del listeners[task_id]
    """

from application.services.tasks_definition.wait_5s import wait_5s

async def consumer():
    logging.info("LOL!!!!")
    try:
        cm = await TASK_MAP["wait_5s"](task_id="LOL!")
        logging.info("in")
        logging.info(cm.get_name())
        await sleep(15)
    except Exception as e:
        logging.error(e)
    return

    with app.app_context():
        # queue_tasks = task_service.queue_tasks
        repository = task_service.repository
        listeners = {}
        # while True:
        from application.models.models import Task
        queued_tasks: Sequence[Message] = [
            Message(body="6494fe71-7505-4415-bc5a-4d16e855ea02"),
        ]

        for queued_task in queued_tasks:
            task_id = queued_task.body
            task_record = repository.get(pk=task_id)
            if task_record is None:
                logging.warning(f"Record not found: {task_id}")
            else:
                logging.info(
                    f"task getting {task_record.name} [{task_record.status.name}]-> {task_id}"
                )

                if task_record.name in TASK_MAP:
                    # repository.mark_running(obj=task_record)
                    async with asyncio.timeout(0.1):
                        listener = await TASK_MAP[task_record.name](task_id=task_id)
                        logging.info("LOL!!!!")
                    logging.info("LOL2!!!!")

                    # listener.add_done_callback(
                    #     partial(finished_callback, repository=repository)
                    # )
                    # listeners[task_id] = listener
                else:
                    # repository.mark_failed(obj=task_record)
                    logging.info(f"Invalid task {task_record.name}")

            # queue_tasks.delete(message=queued_task)


        logging.info(f"{listener.done()} {listener.cancelled()}   {listener}, {type(listener)} {dir(listener)}")
        # currently is needed!
        # somehow the listeners are loosing the track of the task.
        await sleep(5)
        logging.info(f"{listener.done()} {listener.cancelled()}   {listener}, {type(listener)} {dir(listener)}")
        # currently is needed!
        # somehow the listeners are loosing the track of the task.
        await sleep(10)
