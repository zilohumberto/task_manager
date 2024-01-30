import boto3
from typing import Sequence

from settings.default import MAX_TIMEOUT_SECONDS
from application.services.queue.models import Message


class QueueHandler:
    queue = None
    queue_url: str = None

    def __init__(self, **kwargs):
        region_name = kwargs.get("AWS_SQS_REGION_NAME")
        self.queue_url = kwargs.get("QUEUE_URL")
        self.queue = boto3.client("sqs", region_name=region_name)

    def send(self, message: Message):
        response = self.queue.send_message(
            QueueUrl=self.queue_url,
            DelaySeconds=message.delay_seconds,
            MessageBody=message.body,
            MessageAttributes={},
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
            data.append(Message(body=body, receipt_handle=receipt_handle))
        return data

    def delete(self, message: Message):
        self.queue.delete_message(
            QueueUrl=self.queue_url, ReceiptHandle=message.receipt_handle
        )
