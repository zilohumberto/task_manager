from typing import Optional
from dataclasses import dataclass


@dataclass
class Message:
    body: str
    delay_seconds: int = 1
    receipt_handle: Optional[str] = None
