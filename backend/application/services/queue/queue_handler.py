import boto3
from typing import Sequence, Optional


class QueueHandler:
    queue = None
    queue_url: str = None

    def __init__(self, **kwargs):
        region_name = kwargs.get("AWS_SQS_REGION_NAME")
        self.queue_url = kwargs.get("QUEUE_URL")
        self.queue = boto3.client("sqs", region_name=region_name)

    def send(self, body: str):
        response = self.queue.send_message(
            QueueUrl=self.queue_url,
            DelaySeconds=1,
            MessageBody=body,
        )
        print("message sent to the queue", response["MessageId"])

    def receive(self) -> Optional[Sequence[tuple]]:
        response = self.queue.receive_message(
            QueueUrl=self.queue_url,
            AttributeNames=["SentTimestamp"],
            MaxNumberOfMessages=10,
            MessageAttributeNames=["All"],
            VisibilityTimeout=5,
            WaitTimeSeconds=0,
        )
        data = []
        msgs = response.get("Messages") or []
        for msg in msgs:
            receipt_handle = msg["ReceiptHandle"]
            body = msg["Body"]
            data.append((body, receipt_handle))
        return data

    def delete(self, pk: str):
        self.queue.delete_message(QueueUrl=self.queue_url, ReceiptHandle=pk)
