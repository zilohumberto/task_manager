import boto3
from typing import Sequence

from settings.default import MAX_TIMEOUT_SECONDS, AWS_SQS_REGION_NAME
from application.services.queue.models import Message
from service.storages.queue_base import QueueBase

class SQS(QueueBase):
    queue = None
    queue_url: str = None

    def __init__(self, queue_url, **kwargs):
        super(SQS, self).__init__(queue_url, **kwargs)
        self.queue = boto3.client("sqs", region_name=AWS_SQS_REGION_NAME)

    def send(self, message: Message, **kwargs):
        response = self.queue.send_message(
            QueueUrl=self.queue_url,
            DelaySeconds=message.delay_seconds,
            MessageBody=message.body,
            MessageAttributes={
                "kind": {"DataType": "String", "StringValue": message.kind.name}
            },
        )
        print("message sent to the queue", response["MessageId"])

    def receive(self) -> Sequence[Message]:
        response = self.queue.receive_message(
            QueueUrl=self.queue_url,
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
        self.queue.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message.receipt_handle)
