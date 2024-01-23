from flask import request, jsonify

from app import app
from application.services.task_services import TaskService
from application.repositories.persistance.task_db_repository import TaskDBRepository


task_service = TaskService(
    task_repository=TaskDBRepository(),
    AWS_SQS_REGION_NAME=app.config.get("AWS_SQS_REGION_NAME"),
    QUEUE_URL=app.config.get("QUEUE_URL"),
)


@app.route("/ping")
def ping():
    return jsonify({"message": "pong"})


@app.route("/", methods=["GET"])
def get_tasks():
    """
    get details of all tasks
    """
    return jsonify({"data": task_service.get_all()}), 200


@app.route("/", methods=["POST"])
def create_task():
    """
    create an async task
    """
    data = request.json
    task_name = data.get("name")
    task_id = task_service.push_task(task_name=task_name)
    return jsonify({"task_id": task_id}), 201


@app.route("/<string:task_id>", methods=["GET"])
def retrieve_task(task_id: str):
    """
    Get details (status) of <task_id> 
    expected status code: 200
    response:
        {data: <task details>}
    """
    task_instance = task_service.get(task_id=task_id)
    if task_instance:
        return jsonify({"data": task_instance}), 200
    else:
        return jsonify({"message": f"No data for {task_id}"}), 404
