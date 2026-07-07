from flask import Blueprint, abort, jsonify, request

from app.extensions import db
from app.models import Task

api = Blueprint("api", __name__)


@api.get("/")
def index() -> str:
    return "Flask app is running"


@api.get("/api/tasks")
def list_tasks():
    tasks = Task.query.order_by(Task.id.asc()).all()
    return jsonify([task.to_dict() for task in tasks]), 200


@api.post("/api/tasks")
def create_task():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    title = payload.get("title")
    description = payload.get("description")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Field 'title' is required and must be a non-empty string."}), 400

    if description is not None and not isinstance(description, str):
        return jsonify({"error": "Field 'description' must be a string when provided."}), 400

    task = Task(title=title.strip(), description=description)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@api.get("/api/tasks/<int:task_id>")
def get_task(task_id: int):
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404)
    return jsonify(task.to_dict()), 200


@api.patch("/api/tasks/<int:task_id>")
def update_task(task_id: int):
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404)
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    if "title" in payload:
        title = payload["title"]
        if not isinstance(title, str) or not title.strip():
            return jsonify({"error": "Field 'title' must be a non-empty string."}), 400
        task.title = title.strip()

    if "description" in payload:
        description = payload["description"]
        if description is not None and not isinstance(description, str):
            return jsonify({"error": "Field 'description' must be a string or null."}), 400
        task.description = description

    if "completed" in payload:
        completed = payload["completed"]
        if not isinstance(completed, bool):
            return jsonify({"error": "Field 'completed' must be a boolean."}), 400
        task.completed = completed

    db.session.commit()
    return jsonify(task.to_dict()), 200


@api.delete("/api/tasks/<int:task_id>")
def delete_task(task_id: int):
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404)

    db.session.delete(task)
    db.session.commit()
    return "", 204
