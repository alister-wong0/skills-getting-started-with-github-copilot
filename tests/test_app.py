from fastapi.testclient import TestClient

from src.app import activities, app


def test_unregister_participant_removes_email_from_activity():
    client = TestClient(app)
    original_participants = activities["Chess Club"]["participants"][:]

    try:
        response = client.delete(
            "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"

        refreshed = client.get("/activities").json()
        assert "michael@mergington.edu" not in refreshed["Chess Club"]["participants"]
    finally:
        activities["Chess Club"]["participants"] = original_participants
