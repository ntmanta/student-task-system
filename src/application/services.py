"""Application layer: use cases that connect the rules to the repositories."""
from src.domain.errors import DuplicateError, NotFoundError
from src.domain.models import Student, Submission, Task, parse_date
from src.domain.rules import completion_rate, compute_status


class StudentService:
    def __init__(self, students):
        self.students = students

    def add_student(self, data):
        student = Student(
            student_number=data.get("student_number"),
            name=data.get("name"),
            email=data.get("email"),
            course=data.get("course"),
        )
        return self.students.add(student)

    def list_students(self):
        return self.students.list()

    def get_student(self, student_id):
        student = self.students.get(student_id)
        if student is None:
            raise NotFoundError("Student not found")
        return student

    def update_student(self, student_id, data):
        existing = self.get_student(student_id)
        updated = Student(
            id=student_id,
            student_number=data.get("student_number", existing.student_number),
            name=data.get("name", existing.name),
            email=data.get("email", existing.email),
            course=data.get("course", existing.course),
        )
        self.students.update(updated)
        return updated

    def delete_student(self, student_id):
        if not self.students.delete(student_id):
            raise NotFoundError("Student not found")


class TaskService:
    def __init__(self, tasks):
        self.tasks = tasks

    def add_task(self, data):
        task = Task(
            title=data.get("title"),
            description=data.get("description", ""),
            deadline=data.get("deadline"),
        )
        return self.tasks.add(task)

    def list_tasks(self):
        return self.tasks.list()

    def get_task(self, task_id):
        task = self.tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task not found")
        return task

    def delete_task(self, task_id):
        if not self.tasks.delete(task_id):
            raise NotFoundError("Task not found")


class SubmissionService:
    def __init__(self, submissions, students, tasks):
        self.submissions = submissions
        self.students = students
        self.tasks = tasks

    def record_submission(self, student_id, task_id, submitted_on):
        if self.students.get(student_id) is None:
            raise NotFoundError("Student not found")
        task = self.tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task not found")
        submitted_date = parse_date(submitted_on, "Submission date")
        status = compute_status(task.deadline, submitted_date)
        submission = Submission(
            student_id=student_id,
            task_id=task_id,
            submitted_on=submitted_date,
            status=status,
        )
        return self.submissions.add(submission)

    def list_for_task(self, task_id):
        if self.tasks.get(task_id) is None:
            raise NotFoundError("Task not found")
        return self.submissions.list_by_task(task_id)

    def task_report(self, task_id):
        task = self.tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task not found")
        subs = self.submissions.list_by_task(task_id)
        total = self.students.count()
        submitted = len(subs)
        late = sum(1 for s in subs if s.status == "Late")
        return {
            "task_id": task.id,
            "title": task.title,
            "total_students": total,
            "submitted": submitted,
            "late": late,
            "pending": max(total - submitted, 0),
            "completion_rate": completion_rate(submitted, total),
        }