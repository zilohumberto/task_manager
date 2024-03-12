import asyncio
from functools import partial
from typing import Optional

from app import task_service, app, logging
from service.tasks import TASK_MAP
from settings.default import PREFIX_TASK_NAME
from service.storages.queue_handler import QueueHandler


class Worker:
    _loop: Optional[asyncio.AbstractEventLoop] = None
    running: bool = None
    max_queue_parallel_messages: int = None
    _repository = None
    _queue_handler = None

    def __init__(self, max_queue_parallel_messages: int = 10):
        self._loop = None
        self.running = False
        self.max_queue_parallel_messages = max_queue_parallel_messages
        self._repository = task_service.repository
        self._queue_handler = QueueHandler(
            queue=task_service.queue_tasks,
            repository=task_service.repository,
        )

    def _stop_worker(self):
        self.running = False
        self._queue_handler.stop()
        self._loop.stop()
        # control + c
        # asyncio event
        # threading event

    def _finish_message(self, async_task_name: str, task_id: str):
        logging.info(f"Marking {async_task_name} as done!!!!!")
        self._repository.mark_done(pk=task_id)

    def create_tasks(self, tg, task_name: str, task_id: str):
        coroutine = TASK_MAP[task_name](task_id=task_id)
        task_name = f"{PREFIX_TASK_NAME}_{task_name}_{task_id}"
        logging.info(f"Created Coroutine {type(coroutine)}({task_name})")
        self._repository.mark_running(pk=task_id)
        task = tg.create_task(coroutine, name=task_name)
        task.add_done_callback(
            partial(
                self._finish_message,
                task_id=task_id,
            )
        )
        return task

    async def _poll_messages(self):
        logging.info("Started polling")
        try:
            while self.running:
                tasks = []
                async with asyncio.TaskGroup() as tg:
                    logging.info("Previous call pull()")
                    task_generator = self._queue_handler.pull()
                    while self.running:
                        task_record = next(task_generator)
                        if task_record is None:
                             break
                        logging.info(f"found a task record to process")
                        task = self.create_tasks(
                             tg, task_name=task_record.name, task_id=task_record.id,
                        )
                        logging.info(f"Coroutine({task.get_name()}) IsDone={task.done()}")
                        tasks.append(task)

                logging.info(f"Number of task(s) processed {len(tasks)}")

        except Exception as e:
            logging.error(e)
            logging.warning("Impossible to recover, stopping polling!")
            self._stop_worker()

    def start(self, event_loop: asyncio.AbstractEventLoop = None):
        app.app_context().push()
        logging.info("starting worker")
        self.running = True
        loop = event_loop or asyncio.get_event_loop()
        self._loop = loop

        if self._loop and self._loop.is_closed():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

        loop.create_task(self._poll_messages())
        self._loop.run_forever()
