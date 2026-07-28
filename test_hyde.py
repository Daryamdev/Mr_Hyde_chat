from fastapi.testclient import TestClient
from hyde import app
import os
from unittest.mock import AsyncMock, patch


for filename in ["memory.txt", "prompt.txt"]:
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("")
client= TestClient(app)

def  test_read_main():
    response = client.get("/")
    assert response.status_code == 200


from unittest.mock import AsyncMock, patch

def test_chat_endpoint():
    mock_response = AsyncMock()
    mock_response.content = [AsyncMock(text="Hi Hyde")]

    # Подменяем реальный вызов к API на заглушку
    with patch("hyde.client.messages.create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = mock_response

        
        response = client.post("/chat", json={"user_input": "Hello"})
        
        
        assert response.status_code == 200