import boto3
from typing import Sequence, Optional

from settings.default import MAX_TIMEOUT_SECONDS


class QueueHandler:
    queue = None
    queue_url: str = None

    def __init__(self, **kwargs):
        region_name = kwargs.get("AWS_SQS_REGION_NAME")
        self.queue_url = kwargs.get("QUEUE_URL")
        self.queue = boto3.client("sqs", region_name=region_name)

    def send(self, body: str, kind: str = "task", **kwargs):
        response = self.queue.send_message(
            QueueUrl=self.queue_url,
            DelaySeconds=1 if kind == "task" else MAX_TIMEOUT_SECONDS,
            MessageBody=body,
            MessageAttributes={
                "kind": {"DataType": "String", "StringValue": kind}
            },
        )
        print("message sent to the queue", response["MessageId"])

    def receive(self) -> Optional[Sequence[dict]]:
        response = self.queue.receive_message(
            QueueUrl=self.queue_url,
            AttributeNames=["SentTimestamp"],
            MaxNumberOfMessages=10,
            MessageAttributeNames=["All"],
            VisibilityTimeout=MAX_TIMEOUT_SECONDS,
            WaitTimeSeconds=10,
        )
        data = []
        msgs = response.get("Messages") or []
        for msg in msgs:
            receipt_handle = msg["ReceiptHandle"]
            body = msg["Body"]
            attrs = {key: value.get("StringValue") for key, value in msg.get("MessageAttributes").items()}
            data.append(dict(body=body, receipt_handle=receipt_handle, **attrs))
        return data

    def delete(self, pk: str):
        self.queue.delete_message(QueueUrl=self.queue_url, ReceiptHandle=pk)
