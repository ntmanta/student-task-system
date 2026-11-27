"""Domain entities: Student, Task and Submission."""
from dataclasses import dataclass
from datetime import date
from typing import Optional

from src.domain.errors import ValidationError


def parse_date(value, field_name="Date"):
    """Accept a date object or a YYYY-MM-DD string and return a date."""
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        raise ValidationError(f"{field_name} must be in YYYY-MM-DD format")


@dataclass
class Student:
    student_number: str
    name: str
    email: str
    course: str
    id: Optional[int] = None

    def __post_init__(self):
        self.student_number = str(self.student_number or "").strip()
        self.name = str(self.name or "").strip()
        self.email = str(self.email or "").strip()
        self.course = str(self.course or "").strip()
        if not self.student_number:
            raise ValidationError("Student number is required")
        if not self.name:
            raise ValidationError("Name is required")
        local, _, domain = self.email.partition("@")
        if not local or "." not in domain:
            raise ValidationError("A valid email is required")
        if not self.course:
            raise ValidationError("Course is required")


@dataclass
class Task:
    title: str
    deadline: date
    description: str = ""
    id: Optional[int] = None

    def __post_init__(self):
        self.title = str(self.title or "").strip()
        self.description = str(self.description or "").strip()
        if not self.title:
            raise ValidationError("Task title is required")
        self.deadline = parse_date(self.deadline, "Deadline")


@dataclass
class Submission:
    student_id: int
    task_id: int
    submitted_on: date
    status: str = "Submitted"
    id: Optional[int] = None

    def __post_init__(self):
        self.submitted_on = parse_date(self.submitted_on, "Submission date")