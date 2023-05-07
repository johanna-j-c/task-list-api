from flask import Blueprint, make_response, jsonify
from app.models.goal import Goal

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    goal_list = [goal.to_dict() for goal in goals]

    return make_response(jsonify(goal_list), 200)