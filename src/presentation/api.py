"""Presentation layer: Flask REST API and the web page."""
from flask import Flask, jsonify, render_template, request

from src.application.services import StudentService, SubmissionService, TaskService
from src.domain.errors import DuplicateError, NotFoundError, ValidationError
from src.infrastructure.database import Database
from src.infrastructure.repositories import (
    StudentRepository,
    SubmissionRepository,
    TaskRepository,
)


def student_dict(s):
    return {
        "id": s.id,
        "student_number": s.student_number,
        "name": s.name,
        "email": s.email,
        "course": s.course,
    }


def task_dict(t):
    return {
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "deadline": t.deadline.isoformat(),
    }


def submission_dict(s):
    return {
        "id": s.id,
        "student_id": s.student_id,
        "task_id": s.task_id,
        "submitted_on": s.submitted_on.isoformat(),
        "status": s.status,
    }


def create_app(db_path="student_tasks.db"):
    app = Flask(__name__, template_folder="templates")

    db = Database(db_path)
    student_repo = StudentRepository(db)
    task_repo = TaskRepository(db)
    submission_repo = SubmissionRepository(db)

    students = StudentService(student_repo)
    tasks = TaskService(task_repo)
    submissions = SubmissionService(submission_repo, student_repo, task_repo)

    @app.errorhandler(ValidationError)
    def handle_validation(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(NotFoundError)
    def handle_not_found(e):
        return jsonify({"error": str(e)}), 404

    @app.errorhandler(DuplicateError)
    def handle_duplicate(e):
        return jsonify({"error": str(e)}), 409

    @app.route("/")
    def home():
        return render_template("index.html")

    # ---------- Students ----------
    @app.route("/api/students", methods=["GET"])
    def list_students():
        return jsonify([student_dict(s) for s in students.list_students()])

    @app.route("/api/students", methods=["POST"])
    def add_student():
        data = request.get_json(silent=True) or {}
        return jsonify(student_dict(students.add_student(data))), 201

    @app.route("/api/students/<int:student_id>", methods=["GET"])
    def get_student(student_id):
        return jsonify(student_dict(students.get_student(student_id)))

    @app.route("/api/students/<int:student_id>", methods=["PUT"])
    def update_student(student_id):
        data = request.get_json(silent=True) or {}
        return jsonify(student_dict(students.update_student(student_id, data)))

    @app.route("/api/students/<int:student_id>", methods=["DELETE"])
    def delete_student(student_id):
        students.delete_student(student_id)
        return jsonify({"message": "Student deleted"})

    # ---------- Tasks ----------
    @app.route("/api/tasks", methods=["GET"])
    def list_tasks():
        return jsonify([task_dict(t) for t in tasks.list_tasks()])

    @app.route("/api/tasks", methods=["POST"])
    def add_task():
        data = request.get_json(silent=True) or {}
        return jsonify(task_dict(tasks.add_task(data))), 201

    @app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id):
        tasks.delete_task(task_id)
        return jsonify({"message": "Task deleted"})

    # ---------- Submissions ----------
    @app.route("/api/submissions", methods=["POST"])
    def record_submission():
        data = request.get_json(silent=True) or {}
        sub = submissions.record_submission(
            data.get("student_id"), data.get("task_id"), data.get("submitted_on")
        )
        return jsonify(submission_dict(sub)), 201

    @app.route("/api/tasks/<int:task_id>/submissions", methods=["GET"])
    def task_submissions(task_id):
        return jsonify([submission_dict(s) for s in submissions.list_for_task(task_id)])

    @app.route("/api/tasks/<int:task_id>/report", methods=["GET"])
    def task_report(task_id):
        return jsonify(submissions.task_report(task_id))

    return app