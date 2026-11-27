"""Flask REST API: translates HTTP requests into service calls."""
from datetime import date

from flask import Flask, jsonify, request

from src.application.services import StudentService, SubmissionService, TaskService
from src.domain.errors import DuplicateError, NotFoundError, ValidationError
from src.infrastructure.database import Database
from src.infrastructure.repositories import (
    StudentRepository,
    SubmissionRepository,
    TaskRepository,
)


def student_json(s):
    return {
        "id": s.id,
        "student_number": s.student_number,
        "name": s.name,
        "email": s.email,
        "course": s.course,
    }


def task_json(t):
    return {
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "deadline": t.deadline.isoformat(),
    }


def submission_json(s):
    return {
        "id": s.id,
        "student_id": s.student_id,
        "task_id": s.task_id,
        "submitted_on": s.submitted_on.isoformat(),
        "status": s.status,
    }


def create_app(db_path="student_task.db"):
    app = Flask(__name__)
    db = Database(db_path)

    student_repo = StudentRepository(db)
    task_repo = TaskRepository(db)
    submission_repo = SubmissionRepository(db)

    students = StudentService(student_repo)
    tasks = TaskService(task_repo)
    submissions = SubmissionService(student_repo, task_repo, submission_repo)

    @app.errorhandler(ValidationError)
    def handle_validation(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(NotFoundError)
    def handle_not_found(e):
        return jsonify({"error": str(e)}), 404

    @app.errorhandler(DuplicateError)
    def handle_duplicate(e):
        return jsonify({"error": str(e)}), 409

    @app.get("/")
    def index():
        return jsonify({"message": "Student Task System API"})

    # ---- Students ----
    @app.post("/students")
    def add_student():
        d = request.get_json(silent=True) or {}
        s = students.add_student(
            d.get("student_number"), d.get("name"), d.get("email"), d.get("course")
        )
        return jsonify(student_json(s)), 201

    @app.get("/students")
    def list_students():
        return jsonify([student_json(s) for s in students.list_students()])

    @app.get("/students/<int:student_id>")
    def get_student(student_id):
        return jsonify(student_json(students.get_student(student_id)))

    @app.put("/students/<int:student_id>")
    def update_student(student_id):
        d = request.get_json(silent=True) or {}
        s = students.update_student(
            student_id,
            d.get("student_number"),
            d.get("name"),
            d.get("email"),
            d.get("course"),
        )
        return jsonify(student_json(s))

    @app.delete("/students/<int:student_id>")
    def delete_student(student_id):
        students.delete_student(student_id)
        return "", 204

    # ---- Tasks ----
    @app.post("/tasks")
    def add_task():
        d = request.get_json(silent=True) or {}
        t = tasks.add_task(d.get("title"), d.get("deadline"), d.get("description", ""))
        return jsonify(task_json(t)), 201

    @app.get("/tasks")
    def list_tasks():
        return jsonify([task_json(t) for t in tasks.list_tasks()])

    @app.get("/tasks/<int:task_id>")
    def get_task(task_id):
        return jsonify(task_json(tasks.get_task(task_id)))

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id):
        tasks.delete_task(task_id)
        return "", 204

    # ---- Submissions and report ----
    @app.post("/submissions")
    def submit():
        d = request.get_json(silent=True) or {}
        sub = submissions.submit(
            d.get("student_id"),
            d.get("task_id"),
            d.get("submitted_on") or date.today().isoformat(),
        )
        return jsonify(submission_json(sub)), 201

    @app.get("/tasks/<int:task_id>/report")
    def report(task_id):
        return jsonify(submissions.report(task_id))

    return app