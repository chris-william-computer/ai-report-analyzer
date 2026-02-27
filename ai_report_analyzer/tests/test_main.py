from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/reports")
    assert response.status_code == 200

def test_upload_report_failure():
    response = client.post("/upload")
    assert response.status_code == 422