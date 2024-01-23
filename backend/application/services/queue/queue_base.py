from typing import Sequence, Optional


class QueueBase:
    queue = None
    queue_url: str = None

    def __init__(self):
        pass

    def send(self, body: str):
        raise NotImplementedError()

    def receive(self) -> Optional[Sequence[tuple]]:
        raise NotImplementedError()

    def delete(self, pk: str):
        raise NotImplementedError()
