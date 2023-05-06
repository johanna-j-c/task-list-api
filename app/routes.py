from flask import Blueprint, request, jsonify, make_response, abort
from app.models.task import Task

task_bp = Blueprint("tasks", __name__,url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"]
    )

    message = f"Task {new_task.title} successfully created"
    return make_response(message, 201)
        