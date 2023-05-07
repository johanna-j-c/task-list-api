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

        return make_response({"task":new_task.to_dict()}, 201)
    
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        message = f"{cls.__name__} {model_id} is not valid"
        abort(make_response({"message":message}, 400))
    
    model = cls.query.get(model_id)

    if not model:
        message = f"{cls.__name__} {model_id} not found"
        abort(make_response({"message":message}, 404))
    
    return model

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    task_list = [task.to_dict() for task in tasks]
    
    return make_response(jsonify(task_list), 200)

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return make_response({"task":task.to_dict()}, 200)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task_data = request.get_json()
    task_to_update = validate_model(Task, task_id)

    task_to_update.title = task_data["title"]
    task_to_update.description = task_data["description"]
    # will need to update completed_at attribute in wave 3

    db.session.commit()

    return make_response({"task":task_to_update.to_dict()}, 200)

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task_to_delete = validate_model(Task, task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    message = f'Task {task_id} "{task_to_delete.title}" successfully deleted'
    return make_response({"details":message}, 200)