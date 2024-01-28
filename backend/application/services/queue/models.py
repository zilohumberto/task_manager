from typing import Optional
from dataclasses import dataclass
from enum import Enum


class MessageKind(Enum):
    task = "TASK"
    health_check = "HEALTH_CHECK"


@dataclass
class Message:
    body: str
    kind: MessageKind = MessageKind.task
    delay_seconds: int = 1
    receipt_handle: Optional[str] = None
