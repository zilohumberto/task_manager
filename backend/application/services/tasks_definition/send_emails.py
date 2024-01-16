from application.services.queue.handler import task


@task(task_name="send_emails")
async def send_emails():
    pass
