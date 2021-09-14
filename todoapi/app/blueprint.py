""" This module contains the 'index' Blueprint which organize and
group, views related to the index endpoint of HTTP REST API.
"""

from flask import Blueprint
from flask import jsonify, make_response

from app.model import Task

bp = Blueprint("index", __name__, url_prefix="")


@bp.route("/", methods=["GET"])
def index():
    """
    Return a task list.
    GET /api/v1.0/task
    """

    tasks = Task.query.all()
    return make_response(jsonify([task.serialize() for task in tasks]), 200)
