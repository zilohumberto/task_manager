from app import app
from flask import request, jsonify, redirect

from backend.application.services.queue.push import push_task


@app.route("/ping")
def ping():
    return jsonify({"message": "pong"})


@app.route("/", methods=["GET"])
def get_tasks():
    """
    get details of all tasks
    """
    return jsonify({"data": []}), 200


@app.route("/", methods=["POST"])
def create_task():
    """
    create an async task
    """
    data = request.json()
    task_name = data.get("name")
    return jsonify({"data": push_task(task_name)}), 201


@app.route("/<string:task_id>", methods=["GET"])
def retrieve_task(task_id):
    """
    Get details (status) of <task_id> 
    expected status code: 200
    response:
        {data: <task details>}
    """
    return jsonify({"data": None}), 200
