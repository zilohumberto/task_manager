from dataclasses import dataclass
from uuid import UUID
from datetime import datetime, timedelta
from typing import Optional
from backend.application.models.enums import TaskStatus
from asyncio import tasks
from backend.settings.default import MAX_TIMEOUT_SECONDS


@dataclass
class Task:
    _id: UUID 
    listener: tasks.Task
    name: str 
    start_time: datetime  # start time when arrive to the queue: TBD
    end_time: Optional[datetime] = None
    exec_start_time: Optional[datetime] = None
    status: TaskStatus = TaskStatus.CREATED

    def set_name(self):
        self.listener.set_name(self._id)

    def mark_running(self):
        self.status = TaskStatus.RUNNING
        self.exec_start_time = datetime.utcnow()

    def mark_done(self):
        self.status = TaskStatus.DONE
        self.end_time = datetime.utcnow()

    def mark_cancelled(self):
        self.status = TaskStatus.CANCELLED
        self.listener.cancel()
        self.end_time = self.end_time

    def mark_failed(self):
        self.status = TaskStatus.FAILED
        self.end_time = self.end_time

    def check_timeout(self) -> bool:
        time_difference = datetime.utcnow() - self.start_time
        if time_difference >= timedelta(seconds=MAX_TIMEOUT_SECONDS):
            # force cancel due timeout!
            return True
        return False
