from typing import Optional, Sequence

from application.models.models import Task


class TaskRepository:
    model = Task

    def __init__(self):
        pass

    def get(self, pk: str) -> Optional[Task]:
        raise NotImplementedError()

    def create(self, obj: Task) -> Optional[Task]:
        raise NotImplementedError()

    def filter(self, **kwargs) -> Sequence[Task]:
        raise NotImplementedError()

    def delete(self, **kwargs):
        raise NotImplementedError()

    def save(self, obj: Task):
        raise NotImplementedError()

    def mark_running(self, pk: str = None, obj: Task = None):
        raise NotImplementedError()

    def mark_done(self, pk: str = None, obj: Task = None):
        raise NotImplementedError()

    def mark_cancelled(self, pk: str = None, obj: Task = None):
        raise NotImplementedError()

    def mark_failed(self, pk: str = None, obj: Task = None):
        raise NotImplementedError()
