from service.tasks.resources import task


@task(task_name="send_emails")
async def send_emails(**kwargs):
    pass
