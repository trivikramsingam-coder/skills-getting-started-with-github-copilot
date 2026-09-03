from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_get_activities_returns_activity_data():
    response = client.get("/activities")

    assert response.status_code == 200
    assert "Chess Club" in response.json()


def test_signup_adds_student_to_activity():
    email = "step4-signup@example.com"

    try:
        response = client.post("/activities/Basketball Team/signup", params={"email": email})

        assert response.status_code == 200
        assert email in activities["Basketball Team"]["participants"]
    finally:
        if email in activities["Basketball Team"]["participants"]:
            activities["Basketball Team"]["participants"].remove(email)


def test_duplicate_signup_is_rejected():
    email = "step4-duplicate@example.com"
    participants = activities["Basketball Team"]["participants"]
    participants.append(email)

    try:
        response = client.post("/activities/Basketball Team/signup", params={"email": email})

        assert response.status_code == 400
        assert response.json()["detail"] == "Student is already signed up"
    finally:
        participants.remove(email)


def test_unregister_removes_student():
    email = "step4-unregister@example.com"
    participants = activities["Basketball Team"]["participants"]
    participants.append(email)

    response = client.delete(f"/activities/Basketball Team/participants/{email}")

    assert response.status_code == 200
    assert email not in participants


def test_unknown_activity_returns_not_found():
    response = client.post("/activities/Unknown Activity/signup", params={"email": "student@example.com"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
