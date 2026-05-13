import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi.testclient import TestClient
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set dummy environment variables for config validation
os.environ["QDRANT_URL"] = "http://localhost:6333"
os.environ["DATABASE_URL"] = "postgresql://user:pass@localhost:5432/db"
os.environ["LLM_API_KEY"] = "sk-dummy"

# Mock external dependencies before importing the app
with patch('utils.database.db.create_pool', new_callable=AsyncMock), \
     patch('utils.vector_db.vector_db.create_collection', return_value=None), \
     patch('utils.embedding.EmbeddingModel', return_value=MagicMock()), \
     patch('utils.vector_db.VectorDB', return_value=MagicMock()):
    from main import app

client = TestClient(app)

@pytest.fixture
def mock_vector_db():
    with patch('routers.chat.vector_db', new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_embedding_model():
    with patch('routers.chat.embedding_model') as mock:
        yield mock

@pytest.fixture
def mock_db():
    with patch('routers.chat.db', new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_llm_call():
    with patch('routers.chat.call_llm_api', new_callable=AsyncMock) as mock:
        yield mock

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_api_v1_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_chat_endpoint_success(mock_vector_db, mock_embedding_model, mock_llm_call, mock_db):
    # Setup mocks
    mock_embedding_model.encode_single.return_value = [0.1, 0.2, 0.3]
    mock_vector_db.search_vectors.return_value = [
        {"content": "Robot basics content", "chapter": "Chapter 1", "score": 0.9}
    ]
    mock_llm_call.return_value = "This is a mocked AI response."
    mock_db.log_chat_interaction.return_value = {"id": 1, "timestamp": "2023-01-01"}

    # Make request
    response = client.post(
        "/api/v1/chat",
        json={"query": "What are robots?", "session_id": "test-session"}
    )

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "This is a mocked AI response."
    assert "Chapter 1" in data["sources"]
    assert data["session_id"] == "test-session"

    # Verify mock calls
    mock_embedding_model.encode_single.assert_called_once_with("What are robots?")
    mock_vector_db.search_vectors.assert_called_once()
    mock_llm_call.assert_called_once()
    mock_db.log_chat_interaction.assert_called_once()

@pytest.mark.asyncio
async def test_chat_endpoint_no_results(mock_vector_db, mock_embedding_model, mock_db):
    # Setup mocks
    mock_embedding_model.encode_single.return_value = [0.1, 0.2, 0.3]
    mock_vector_db.search_vectors.return_value = []
    mock_db.log_chat_interaction.return_value = {"id": 1, "timestamp": "2023-01-01"}

    # Make request
    response = client.post(
        "/api/v1/chat",
        json={"query": "unrelated query"}
    )

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "couldn't find relevant content" in data["response"]
    assert data["sources"] == []
    assert "session_id" in data

def test_monitoring_usage(mock_db):
    with patch('routers.chat.monitor') as mock_monitor:
        mock_monitor.get_usage_report.return_value = {"request_count": 5}
        mock_monitor.is_near_limits.return_value = False

        response = client.get("/api/v1/monitoring/usage")
        assert response.status_code == 200
        assert response.json()["request_count"] == 5
        assert response.json()["near_limits"] is False
