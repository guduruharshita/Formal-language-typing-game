import pytest
from fastapi.testclient import TestClient

from formal_game.api.main import create_app


@pytest.fixture(scope="module")
def client():
    with TestClient(create_app()) as c:
        yield c


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_start_game_easy(client):
    res = client.post("/api/game/start", json={"difficulty": "easy"})
    assert res.status_code == 200
    data = res.json()
    assert "session_id" in data
    assert data["difficulty"] == "easy"
    assert data["challenge"] is not None
    assert data["score"] == 0


def test_start_game_hard(client):
    res = client.post("/api/game/start", json={"difficulty": "hard"})
    assert res.status_code == 200
    assert res.json()["difficulty"] == "hard"


def test_submit_correct_answer(client):
    start = client.post("/api/game/start", json={"difficulty": "easy"}).json()
    sid = start["session_id"]
    challenge = start["challenge"]
    # Use the provided example — it's always a valid answer for the rule
    res = client.post("/api/game/submit", json={"session_id": sid, "answer": challenge["example"]})
    assert res.status_code == 200
    data = res.json()
    assert data["correct"] is True
    assert data["new_score"] > 0
    assert data["score_delta"] > 0


def test_submit_wrong_answer(client):
    start = client.post("/api/game/start", json={"difficulty": "easy"}).json()
    sid = start["session_id"]
    res = client.post("/api/game/submit", json={"session_id": sid, "answer": "XXXXXXXXXXX"})
    assert res.status_code == 200
    data = res.json()
    assert data["correct"] is False
    assert data["score_delta"] < 0


def test_game_status(client):
    start = client.post("/api/game/start", json={"difficulty": "medium"}).json()
    sid = start["session_id"]
    res = client.get(f"/api/game/status/{sid}")
    assert res.status_code == 200
    data = res.json()
    assert data["session_id"] == sid
    assert data["score"] == 0
    assert data["finished"] is False


def test_session_not_found(client):
    res = client.post("/api/game/submit", json={"session_id": "fake-id", "answer": "a"})
    assert res.status_code == 404


def test_status_not_found(client):
    res = client.get("/api/game/status/fake-id")
    assert res.status_code == 404


def test_list_challenges(client):
    res = client.get("/api/game/challenges")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 10


def test_list_challenges_filter_by_difficulty(client):
    res = client.get("/api/game/challenges?difficulty=hard")
    assert res.status_code == 200
    data = res.json()
    assert all(c["difficulty"] == "hard" for c in data)


def test_list_challenges_filter_by_category(client):
    res = client.get("/api/game/challenges?category=Regular+Language")
    assert res.status_code == 200
    data = res.json()
    assert all(c["category"] == "Regular Language" for c in data)


def test_leaderboard_empty(client):
    res = client.get("/api/leaderboard")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
