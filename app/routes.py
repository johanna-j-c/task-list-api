from flask import Blueprint, request, jsonify, make_response, abort
from app.models.task import Task
from app import db

task_bp = Blueprint("tasks", __name__,url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    try:
        new_task = Task.from_dict(request_body)
        db.session.add(new_task)
        db.session.commit()

        return make_response({
            "task":{
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": False
            }}, 201)
    
    except KeyError as e:
        abort(make_response({"message":f"Missing required value: {e}"}, 400))

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    task_list = []

    for task in tasks:
        task_list.append(dict(
            title=task.title,
            description=task.description,
            completed_at=task.completed_at
        ))
    
    return make_response(jsonify(task_list), 200)