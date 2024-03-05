from application.services.queue.models import Message
from application.repositories.persistance.task_repository import TaskRepository
from service.storages.queue_base import QueueBase
from service.tasks import TASK_MAP


class QueueHandler:
    queue: QueueBase = None
    repository: TaskRepository = None
    _stopped: bool = None

    def __init__(self, queue: QueueBase, repository: TaskRepository, **kwargs):
        self.queue = queue
        self.repository = repository
        self._stopped = False

    @staticmethod
    def _validate_message(task_record):
        if task_record is None:
            # record not found, DB inconsistency
            return False
        if task_record.name in TASK_MAP:
            # ignored due a task not allowed!
            return False
            
        return True

    def _delete(self, message: Message):
        self.queue.delete(message)

    def _pull(self):
        _messages = self.queue.receive()
        task_records = []
        messages = []
        for _message in _messages:
            task_id = _message.body
            task_record = self.repository.get(pk=task_id)
            if self._validate_message(task_record=task_record):
                messages.append(_message)
                task_records.append(task_record)
            else:
                # invalid message
                # TODO: logs
                pass
        yield task_records
        # TODO: weakness, if a task is not processed it will be deleted anyway
        for messages in messages:
            self._delete(message=messages)
        
    def pull(self):
        # if polling stopped, avoid wait and process more messages
        if self._stopped:
            return None

        return self._pull()

    def stop(self):
        self._stopped = True
    