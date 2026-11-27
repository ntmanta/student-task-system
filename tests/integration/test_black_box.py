import pytest

VALID = {"student_number": "2024-0001", "name": "Juan Dela Cruz", "email": "juan@feu.edu.ph", "course": "BSCSSE"}


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        (VALID, 201),
        ({**VALID, "name": ""}, 400),
        ({**VALID, "email": "not-an-email"}, 400),
        ({**VALID, "email": "a@b"}, 400),
        ({**VALID, "student_number": ""}, 400),
        ({**VALID, "course": ""}, 400),
        ({}, 400),
    ],
)
def test_add_student_inputs(client, payload, expected_status):
    assert client.post("/api/students", json=payload).status_code == expected_status


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"title": "Quiz 1", "deadline": "2026-12-01"}, 201),
        ({"title": "", "deadline": "2026-12-01"}, 400),
        ({"title": "Quiz 1", "deadline": ""}, 400),
        ({"title": "Quiz 1", "deadline": "12/01/2026"}, 400),
        ({"title": "Quiz 1"}, 400),
    ],
)
def test_add_task_inputs(client, payload, expected_status):
    assert client.post("/api/tasks", json=payload).status_code == expected_status