from fastapi.testclient import TestClient
from study_sentinel.api import app
client=TestClient(app)
def test_health():
    assert client.get("/health").json()["status"]=="ok"
def test_demo_aggregate_only():
    response=client.post("/demo/summary",json={"n":30,"seed":2})
    assert response.status_code==200
    assert response.json()["participants"]==30
    assert "participant_id" not in response.text
def test_invalid_n():
    assert client.post("/demo/summary",json={"n":5}).status_code==422
