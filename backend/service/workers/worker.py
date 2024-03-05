import asyncio
from datetime import datetime
from functools import partial
from typing import Optional, Sequence

from application.models.models import Task
from application.repositories.persistance.task_db_repository import TaskDBRepository
from service.storages.sqs import SQS
from service.storages.queue_handler import QueueHandler
from service.tasks import TASK_MAP
from settings.default import QUEUE_URL, PREFIX_TASK_NAME


class Worker:
    _loop: Optional[asyncio.AbstractEventLoop] = None
    running: bool = None
    max_queue_parallel_messages: int = None
    repository = None

    def __init__(self, max_queue_parallel_messages: int = 10):
        self._loop = None
        self.running = False
        self.max_queue_parallel_messages = max_queue_parallel_messages
        self.repository = TaskDBRepository()

    def _stop_worker(self):
        self.running = False

    def _finish_message(self, start_time, handler_name: str, task_id: str):
        self.repository.mark_done(pk=task_id)

    def _delete_message(self):
        pass

    def create_tasks(self, tg, task_name: str, task_id: str) -> bool:
        coroutine = TASK_MAP[task_name](task_id=task_id)
        task_name = f"{PREFIX_TASK_NAME}_{task_name}_{task_id}"
        self.repository.mark_running(pk=task_id)
        task = tg.create_task(coroutine, name=task_name)
        task.add_done_callback(
            partial(
                self._finish_message,
                start_time=datetime.utcnow().timestamp(),
                handler_name=task_name,
                task_id=task_id,
            )
        )
        return task

    async def _poll_messages(self):
        queue_instance = SQS(queue_url=QUEUE_URL)
        queue_handler = QueueHandler(queue=queue_instance, repository=self.repository, max_num_of_messages=self.max_queue_parallel_messages)
        while self.running:
            pulled_messages = queue_handler.pull()
            task_records: Sequence[Task] = next(pulled_messages)
            if task_records is None:
                await asyncio.sleep(1)
                continue

            async with asyncio.TaskGroup() as tg:
                tasks = []
                for task_record in task_records:
                    task = self.create_tasks(
                        tg, task_name=task_record.name, task_id=task_record.id,
                    )
                    tasks.append(task)

            next(pulled_messages)  # delete messages

    def start(self, event_loop: asyncio.AbstractEventLoop = None):
        self.running = True
        loop = event_loop or asyncio.get_event_loop()
        self._loop = loop

        if self._loop and self._loop.is_closed():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

        loop.create_task(self._poll_messages())
        self._loop.run_forever()
