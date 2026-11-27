"""Data handling: all SQL lives here."""
import sqlite3

from src.domain.errors import DuplicateError
from src.domain.models import Student, Submission, Task


class StudentRepository:
    def __init__(self, db):
        self.conn = db.conn

    @staticmethod
    def _to_model(row):
        return Student(
            id=row["id"],
            student_number=row["student_number"],
            name=row["name"],
            email=row["email"],
            course=row["course"],
        )

    def add(self, student):
        try:
            cur = self.conn.execute(
                "INSERT INTO students (student_number, name, email, course) VALUES (?, ?, ?, ?)",
                (student.student_number, student.name, student.email, student.course),
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise DuplicateError("Student number already exists")
        student.id = cur.lastrowid
        return student

    def get(self, student_id):
        row = self.conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
        return self._to_model(row) if row else None

    def list(self):
        rows = self.conn.execute("SELECT * FROM students ORDER BY id").fetchall()
        return [self._to_model(r) for r in rows]

    def update(self, student):
        try:
            cur = self.conn.execute(
                "UPDATE students SET student_number = ?, name = ?, email = ?, course = ? WHERE id = ?",
                (student.student_number, student.name, student.email, student.course, student.id),
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise DuplicateError("Student number already exists")
        return cur.rowcount > 0

    def delete(self, student_id):
        cur = self.conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def count(self):
        return self.conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]


class TaskRepository:
    def __init__(self, db):
        self.conn = db.conn

    @staticmethod
    def _to_model(row):
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            deadline=row["deadline"],
        )

    def add(self, task):
        cur = self.conn.execute(
            "INSERT INTO tasks (title, description, deadline) VALUES (?, ?, ?)",
            (task.title, task.description, task.deadline.isoformat()),
        )
        self.conn.commit()
        task.id = cur.lastrowid
        return task

    def get(self, task_id):
        row = self.conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return self._to_model(row) if row else None

    def list(self):
        rows = self.conn.execute("SELECT * FROM tasks ORDER BY deadline, id").fetchall()
        return [self._to_model(r) for r in rows]

    def delete(self, task_id):
        cur = self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        return cur.rowcount > 0


class SubmissionRepository:
    def __init__(self, db):
        self.conn = db.conn

    @staticmethod
    def _to_model(row):
        return Submission(
            id=row["id"],
            student_id=row["student_id"],
            task_id=row["task_id"],
            submitted_on=row["submitted_on"],
            status=row["status"],
        )

    def add(self, submission):
        try:
            cur = self.conn.execute(
                "INSERT INTO submissions (student_id, task_id, submitted_on, status) VALUES (?, ?, ?, ?)",
                (
                    submission.student_id,
                    submission.task_id,
                    submission.submitted_on.isoformat(),
                    submission.status,
                ),
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise DuplicateError("This student already submitted this task")
        submission.id = cur.lastrowid
        return submission

    def list_by_task(self, task_id):
        rows = self.conn.execute(
            "SELECT * FROM submissions WHERE task_id = ? ORDER BY id", (task_id,)
        ).fetchall()
        return [self._to_model(r) for r in rows]