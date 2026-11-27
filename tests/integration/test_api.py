STUDENT = {"student_number": "2024-0001", "name": "Juan Dela Cruz", "email": "juan@feu.edu.ph", "course": "BSCSSE"}


def test_post_student_returns_201(client):
    res = client.post("/api/students", json=STUDENT)
    assert res.status_code == 201
    assert res.get_json()["id"] == 1


def test_get_students_returns_list(client):
    client.post("/api/students", json=STUDENT)
    res = client.get("/api/students")
    assert res.status_code == 200
    assert len(res.get_json()) == 1


def test_get_one_student(client):
    sid = client.post("/api/students", json=STUDENT).get_json()["id"]
    res = client.get(f"/api/students/{sid}")
    assert res.get_json()["name"] == "Juan Dela Cruz"


def test_put_student_updates_record(client):
    sid = client.post("/api/students", json=STUDENT).get_json()["id"]
    res = client.put(f"/api/students/{sid}", json={"name": "Juan Updated"})
    assert res.status_code == 200
    assert client.get(f"/api/students/{sid}").get_json()["name"] == "Juan Updated"


def test_delete_student_removes_record(client):
    sid = client.post("/api/students", json=STUDENT).get_json()["id"]
    assert client.delete(f"/api/students/{sid}").status_code == 200
    assert client.get(f"/api/students/{sid}").status_code == 404


def test_get_missing_student_returns_404(client):
    assert client.get("/api/students/999").status_code == 404


def test_duplicate_student_number_returns_409(client):
    client.post("/api/students", json=STUDENT)
    assert client.post("/api/students", json=STUDENT).status_code == 409


def test_home_page_loads(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Student Information and Task Management System" in res.data


def test_full_submission_flow(client):
    sid = client.post("/api/students", json=STUDENT).get_json()["id"]
    tid = client.post(
        "/api/tasks", json={"title": "Activity 1", "description": "", "deadline": "2026-12-01"}
    ).get_json()["id"]
    res = client.post(
        "/api/submissions", json={"student_id": sid, "task_id": tid, "submitted_on": "2026-12-03"}
    )
    assert res.status_code == 201
    assert res.get_json()["status"] == "Late"
    report = client.get(f"/api/tasks/{tid}/report").get_json()
    assert report["submitted"] == 1
    assert report["late"] == 1
    assert report["completion_rate"] == 100.0