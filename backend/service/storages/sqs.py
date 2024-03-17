import boto3
from typing import Sequence

from settings.default import MAX_TIMEOUT_SECONDS, AWS_SQS_REGION_NAME
from service.storages.models import Message
from service.storages.queue_base import QueueBase

class SQS(QueueBase):
    _queue = None
    _queue_url: str = None

    def __init__(self, queue_url, **kwargs):
        super(SQS, self).__init__(**kwargs)
        self._queue_url = queue_url
        self._queue = boto3.client("sqs", region_name=AWS_SQS_REGION_NAME)

    def send(self, message: Message, **kwargs):
        response = self._queue.send_message(
            QueueUrl=self._queue_url,
            DelaySeconds=message.delay_seconds,
            MessageBody=message.body,
            MessageAttributes={},
        )
        print("message sent to the queue", response["MessageId"])

    def receive(self) -> Sequence[Message]:
        response = self._queue.receive_message(
            QueueUrl=self._queue_url,
            AttributeNames=["SentTimestamp"],
            MaxNumberOfMessages=10,
            MessageAttributeNames=["All"],
            VisibilityTimeout=MAX_TIMEOUT_SECONDS,
            WaitTimeSeconds=10,
        )
        data: list[Message] = []
        msgs = response.get("Messages") or []
        for msg in msgs:
            receipt_handle = msg["ReceiptHandle"]
            body = msg["Body"]
            attrs = msg.get("MessageAttributes") or {}
            data.append(Message(body=body, receipt_handle=receipt_handle, **attrs))
        return data

    def delete(self, message: Message):
        self._queue.delete_message(QueueUrl=self._queue_url, ReceiptHandle=message.receipt_handle)
