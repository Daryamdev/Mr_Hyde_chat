from fastapi.testclient import TestClient
from hyde import app

client= TestClient(app)

def  test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_chat_endpoint():
 response= client.post("/chat", json={"user_input":"Hello"})
 assert response.status_code == 200
 assert "response" in response.json()