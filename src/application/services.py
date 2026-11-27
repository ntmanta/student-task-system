"""Application services: use cases that connect rules and repositories."""
from src.domain.errors import NotFoundError
from src.domain.models import Student, Submission, Task, parse_date
from src.domain.rules import completion_rate, compute_status


class StudentService:
    def __init__(self, student_repo):
        self.students = student_repo

    def add_student(self, student_number, name, email, course):
        student = Student(student_number, name, email, course)
        return self.students.add(student)

    def get_student(self, student_id):
        student = self.students.get(student_id)
        if student is None:
            raise NotFoundError("Student not found")
        return student

    def list_students(self):
        return self.students.list()

    def update_student(self, student_id, student_number, name, email, course):
        student = Student(student_number, name, email, course, id=student_id)
        if not self.students.update(student):
            raise NotFoundError("Student not found")
        return student

    def delete_student(self, student_id):
        if not self.students.delete(student_id):
            raise NotFoundError("Student not found")


class TaskService:
    def __init__(self, task_repo):
        self.tasks = task_repo

    def add_task(self, title, deadline, description=""):
        task = Task(title, deadline, description)
        return self.tasks.add(task)

    def get_task(self, task_id):
        task = self.tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task not found")
        return task

    def list_tasks(self):
        return self.tasks.list()

    def delete_task(self, task_id):
        if not self.tasks.delete(task_id):
            raise NotFoundError("Task not found")


class SubmissionService:
    def __init__(self, student_repo, task_repo, submission_repo):
        self.students = student_repo
        self.tasks = task_repo
        self.submissions = submission_repo

    def submit(self, student_id, task_id, submitted_on):
        if self.students.get(student_id) is None:
            raise NotFoundError("Student not found")
        task = self.tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task not found")
        submitted_on = parse_date(submitted_on, "Submission date")
        status = compute_status(task.deadline, submitted_on)
        submission = Submission(student_id, task_id, submitted_on, status)
        return self.submissions.add(submission)

    def report(self, task_id):
        task = self.tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task not found")
        subs = self.submissions.list_by_task(task_id)
        total = self.students.count()
        return {
            "task": task.title,
            "total_students": total,
            "submitted_count": len(subs),
            "late_count": sum(1 for s in subs if s.status == "Late"),
            "completion_rate": completion_rate(len(subs), total),
        }