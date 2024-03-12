from typing import Sequence
from service.storages.models import Message


class QueueBase:

    def send(self, message: Message, **kwargs):
        raise NotImplementedError()

    def receive(self) -> Sequence[Message]:
        raise NotImplementedError()

    def delete(self, message: Message):
        raise NotImplementedError()
