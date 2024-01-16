from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from app import db
from application.models.enums import TaskStatus


class Task(db.Model):
    __tablename__ = "task"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    exec_start_time = Column(DateTime)
    status = Column(Enum(TaskStatus), default=TaskStatus.CREATED, nullable=False)
