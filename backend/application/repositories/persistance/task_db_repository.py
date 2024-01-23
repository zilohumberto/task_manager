from sqlalchemy import select
from typing import Optional, Sequence
from datetime import datetime

from app import db
from application.models.models import Task
from application.models.enums import TaskStatus
from application.repositories.persistance.task_repository import TaskRepository


class TaskDBRepository(TaskRepository):
    model = Task

    def get(self, pk: str) -> Optional[Task]:
        stmt = select(Task).where(Task.id == pk)
        result = db.session.execute(stmt).scalar()
        return result

    def create(self, obj: Task) -> Optional[Task]:
        db.session.add(obj)
        db.session.commit()
        return obj

    def filter(self, **kwargs) -> Sequence[Task]:
        stmt = db.session.query(Task)
        if kwargs.get("status"):
            by_status = kwargs.get("status")
            stmt = stmt.filter(Task.status == TaskStatus[by_status])
        results = stmt.all()
        return results

    def delete(self, **kwargs):
        raise NotImplementedError()

    def save(self, obj: Task):
        db.session.commit()
        return obj

    def mark_running(self, pk: str = None, obj: Task = None):
        task = obj or self.get(pk=pk)
        task.status = TaskStatus.RUNNING
        task.exec_start_time = datetime.utcnow()
        self.save(obj=task)

    def mark_done(self, pk: str = None, obj: Task = None):
        task = obj or self.get(pk=pk)
        task.status = TaskStatus.DONE
        task.end_time = datetime.utcnow()
        self.save(obj=task)

    def mark_cancelled(self, pk: str = None, obj: Task = None):
        task = obj or self.get(pk=pk)
        task.status = TaskStatus.CANCELLED
        task.end_time = datetime.utcnow()
        self.save(obj=task)

    def mark_failed(self, pk: str = None, obj: Task = None):
        task = obj or self.get(pk=pk)
        task.status = TaskStatus.FAILED
        task.end_time = datetime.utcnow()
        self.save(obj=task)
