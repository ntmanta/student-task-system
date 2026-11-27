import pytest

from src.application.services import StudentService, SubmissionService, TaskService
from src.domain.errors import DuplicateError, NotFoundError, ValidationError
from src.infrastructure.database import Database
from src.infrastructure.repositories import (
    StudentRepository,
    SubmissionRepository,
    TaskRepository,
)

STUDENT = {"student_number": "2024-0001", "name": "Juan", "email": "juan@feu.edu.ph", "course": "BSCSSE"}


@pytest.fixture
def svc():
    db = Database(":memory:")
    students = StudentRepository(db)
    tasks = TaskRepository(db)
    subs = SubmissionRepository(db)
    return {
        "students": StudentService(students),
        "tasks": TaskService(tasks),
        "subs": SubmissionService(subs, students, tasks),
    }


def test_add_student_returns_id(svc):
    assert svc["students"].add_student(STUDENT).id == 1


def test_duplicate_student_number_is_rejected(svc):
    svc["students"].add_student(STUDENT)
    with pytest.raises(DuplicateError):
        svc["students"].add_student(STUDENT)


def test_update_student_changes_the_name(svc):
    s = svc["students"].add_student(STUDENT)
    updated = svc["students"].update_student(s.id, {"name": "Juan Updated"})
    assert updated.name == "Juan Updated"
    assert svc["students"].get_student(s.id).name == "Juan Updated"


def test_delete_missing_student_raises_not_found(svc):
    with pytest.raises(NotFoundError):
        svc["students"].delete_student(999)


def test_on_time_submission_status(svc):
    s = svc["students"].add_student(STUDENT)
    t = svc["tasks"].add_task({"title": "Quiz", "deadline": "2026-12-01"})
    sub = svc["subs"].record_submission(s.id, t.id, "2026-11-30")
    assert sub.status == "Submitted"


def test_late_submission_status(svc):
    s = svc["students"].add_student(STUDENT)
    t = svc["tasks"].add_task({"title": "Quiz", "deadline": "2026-12-01"})
    sub = svc["subs"].record_submission(s.id, t.id, "2026-12-05")
    assert sub.status == "Late"


def test_same_student_cannot_submit_twice(svc):
    s = svc["students"].add_student(STUDENT)
    t = svc["tasks"].add_task({"title": "Quiz", "deadline": "2026-12-01"})
    svc["subs"].record_submission(s.id, t.id, "2026-11-30")
    with pytest.raises(DuplicateError):
        svc["subs"].record_submission(s.id, t.id, "2026-11-30")


def test_submission_with_bad_date_is_rejected(svc):
    s = svc["students"].add_student(STUDENT)
    t = svc["tasks"].add_task({"title": "Quiz", "deadline": "2026-12-01"})
    with pytest.raises(ValidationError):
        svc["subs"].record_submission(s.id, t.id, "tomorrow")


def test_task_report_counts(svc):
    s1 = svc["students"].add_student(STUDENT)
    svc["students"].add_student({**STUDENT, "student_number": "2024-0002", "name": "Maria"})
    t = svc["tasks"].add_task({"title": "Quiz", "deadline": "2026-12-01"})
    svc["subs"].record_submission(s1.id, t.id, "2026-12-03")
    report = svc["subs"].task_report(t.id)
    assert report["total_students"] == 2
    assert report["submitted"] == 1
    assert report["late"] == 1
    assert report["pending"] == 1
    assert report["completion_rate"] == 50.0