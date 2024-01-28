from typing import Sequence

from application.services.queue.models import Message


class QueueBase:
    queue = None
    queue_url: str = None

    def __init__(self):
        pass

    def send(self, message: Message, **kwargs):
        raise NotImplementedError()

    def receive(self) -> Sequence[Message]:
        raise NotImplementedError()

    def delete(self, message: Message):
        raise NotImplementedError()
