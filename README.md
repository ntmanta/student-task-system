# Student Information and Task Management System

CS0053 Final Project (Group 6). A web application for managing student records, academic tasks, and submissions, with automatic detection of late submissions and per-task completion reports.

## Features

- Add, view, update, and delete student records
- Create and delete tasks with deadlines
- Record submissions; the system marks them **Submitted** or **Late** based on the deadline
- Task report: submitted, pending, late, and completion rate
- REST API with validation and clear error responses

## Tech Stack

- Python 3.11
- Flask (REST API and web page)
- SQLite (database)
- pytest (unit, integration, and black box tests)
- Postman (API testing)
- Git and GitHub, Visual Studio Code

## Architecture

The project follows Clean Architecture and Domain-Driven Design:

```
src/
  domain/          Entities and business rules (Student, Task, Submission)
  application/     Use cases (services)
  infrastructure/  Database and repositories
  presentation/    Flask API and the web page (templates/index.html)
tests/
  unit/            Models, rules, and services
  integration/     API and black box tests
app.py             Entry point
```

## Installation

1. Clone the repository:

```
git clone https://github.com/ntmanta/student-task-system.git
cd student-task-system
```

2. Create and activate a virtual environment (Windows):

```
python -m venv venv
venv\Scripts\activate
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

## Running the Application

```
python app.py
```

Open http://127.0.0.1:5000 in your browser. The database file `student_tasks.db` is created automatically on first run. To start fresh, stop the server (Ctrl + C) and delete `student_tasks.db`.

## Running the Tests

```
python -m pytest -v
```

Expected result: 44 passed (23 unit, 9 integration, 12 black box).

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/students | List all students |
| POST | /api/students | Add a student |
| GET | /api/students/{id} | Get one student |
| PUT | /api/students/{id} | Update a student |
| DELETE | /api/students/{id} | Delete a student |
| GET | /api/tasks | List all tasks |
| POST | /api/tasks | Add a task |
| DELETE | /api/tasks/{id} | Delete a task |
| POST | /api/submissions | Record a submission |
| GET | /api/tasks/{id}/submissions | List submissions for a task |
| GET | /api/tasks/{id}/report | Get the task report |

Status codes: 200 and 201 for success, 400 for invalid input, 404 for a missing record, 409 for a duplicate.

Example request body for `POST /api/students`:

```json
{"student_number": "2024-1001", "name": "Juan Dela Cruz", "email": "juan@feu.edu.ph", "course": "BSCSSE"}
```

## Group Members

- Archimedes Cal
- Timothy Kalingasan
- Norman Manta
- Julian Ordona
- Rafael Silva
