from typing import Optional, Sequence

from backend.application.models.models import Task


class QueueRepository:
    def get(self) -> Optional[Task]:
        raise NotImplementedError()

    def create(self) -> Optional[Task]:
        raise NotImplementedError()

    def filter(self, **kwargs) -> Sequence[Task]:
        raise NotImplementedError()

    def delete(self, **kwargs):
        raise NotImplementedError()

    def is_empty(self):
        raise NotImplementedError()
