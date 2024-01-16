from concurrent.futures import ThreadPoolExecutor
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from functools import partial

app = Flask(__name__)
app.config.from_object("settings.default")
db = SQLAlchemy(app)

from application.views.task_manager import *
from application.services.queue.consumer import consumer


if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        future = executor.submit(
            partial(
                consumer,
                repository=task_service.repository,
                queue_tasks=task_service.queue_tasks,
            )
        )
        app.run(debug=True)
        future.result()
