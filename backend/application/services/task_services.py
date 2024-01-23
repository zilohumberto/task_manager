from datetime import datetime, timedelta
from uuid import uuid4
from typing import Optional, Sequence

from application.services.queue.queue_handler import QueueHandler
from application.repositories.persistance.task_repository import TaskRepository
from application.models.enums import TaskStatus
from settings.default import MAX_TIMEOUT_SECONDS


class TaskService:
    repository: TaskRepository = None
    queue_tasks = None

    def __init__(self, task_repository: TaskRepository, **kwargs):
        self.repository = task_repository
        self.queue_tasks = QueueHandler(
            AWS_SQS_REGION_NAME=kwargs.get("AWS_SQS_REGION_NAME"),
            QUEUE_URL=kwargs.get("QUEUE_URL"),
        )

    def _row_to_dict(self, row: TaskRepository.model) -> dict:
        return dict(id=row.id, status=row.status.name, name=row.name)

    def get_all(self) -> Sequence[dict]:
        rows = self.repository.filter()
        return [self._row_to_dict(row) for row in rows]

    def push_task(self, task_name: str) -> str:
        task = self.repository.model(
            id=uuid4(),
            status=TaskStatus.CREATED,
            name=task_name,
            start_time=datetime.utcnow()
        )
        task = self.repository.create(obj=task)
        self.queue_tasks.send(body=str(task.id))
        return task.id

    def get(self, task_id: str) -> Optional[dict]:
        row = self.repository.get(pk=task_id)
        if row:
            return self._row_to_dict(row)
        else:
            return None

    @staticmethod
    def check_timeout(obj: TaskRepository.model) -> bool:
        time_difference = datetime.utcnow() - obj.exec_start_time
        if time_difference >= timedelta(seconds=MAX_TIMEOUT_SECONDS):
            # need to cancel due timeout!
            return True
        return False
