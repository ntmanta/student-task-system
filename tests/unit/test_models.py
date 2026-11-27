from datetime import date

import pytest

from src.domain.errors import ValidationError
from src.domain.models import Student, Task


def test_valid_student_is_created():
    s = Student("2024-0001", "Juan Dela Cruz", "juan@feu.edu.ph", "BSCSSE")
    assert s.name == "Juan Dela Cruz"


def test_student_name_is_trimmed():
    s = Student("2024-0001", "  Juan  ", "juan@feu.edu.ph", "BSCSSE")
    assert s.name == "Juan"


def test_student_without_name_is_rejected():
    with pytest.raises(ValidationError):
        Student("2024-0001", "", "juan@feu.edu.ph", "BSCSSE")


def test_student_with_invalid_email_is_rejected():
    with pytest.raises(ValidationError):
        Student("2024-0001", "Juan", "not-an-email", "BSCSSE")


def test_student_without_course_is_rejected():
    with pytest.raises(ValidationError):
        Student("2024-0001", "Juan", "juan@feu.edu.ph", "")


def test_task_string_deadline_is_converted_to_date():
    t = Task(title="Quiz 1", deadline="2026-12-01")
    assert t.deadline == date(2026, 12, 1)


def test_task_without_title_is_rejected():
    with pytest.raises(ValidationError):
        Task(title="", deadline="2026-12-01")


def test_task_with_bad_deadline_is_rejected():
    with pytest.raises(ValidationError):
        Task(title="Quiz 1", deadline="12/01/2026")