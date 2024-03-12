from app import logging
from application.repositories.persistance.task_repository import TaskRepository
from service.storages.queue_base import QueueBase
from service.tasks import TASK_MAP


class QueueHandler:
    _queue: QueueBase
    _repository: TaskRepository
    _stopped: bool

    def __init__(self, queue: QueueBase, repository: TaskRepository, **kwargs):
        self._queue = queue
        self._repository = repository
        self._stopped = False

    @staticmethod
    def _validate_message(task_record):
        if task_record is None:
            # record not found, DB inconsistency
            return False
        if task_record.name not in TASK_MAP:
            # ignored due a task not allowed!
            return False
            
        return True

    def _pull(self):
        logging.info("")
        _messages = self._queue.receive()
        logging.info("")
        for _message in _messages:
            if self._stopped:
                break
            task_id = _message.body
            logging.info(f"Task({task_id}) pulled")
            try:
                task_record = self._repository.get(pk=task_id)
            except Exception as e:
                logging.error(e)
                continue
            logging.info(f"TaskRecord({task_record.id} found)")
            if self._validate_message(task_record=task_record):
                yield task_record
                # TODO: weakness, if a task is not processed it will be deleted anyway
                # self._queue.delete(_message)
            else:
                logging.warning(f"Task({task_id}) is invalid!")
        yield None

    def pull(self):
        # if polling stopped, avoid wait and process more messages
        if self._stopped:
            return None

        return self._pull()

    def stop(self):
        self._stopped = True
    