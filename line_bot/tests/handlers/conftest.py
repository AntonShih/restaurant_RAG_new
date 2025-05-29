import os
import pytest
from config import environment
from line_bot.services import user_service

@pytest.fixture
def mock_line_api():
    class MockLineAPI:
        def __init__(self): self.replies = []
        def reply_message(self, request):
            self.replies.append([m.text for m in request.messages])
    return MockLineAPI()

@pytest.fixture
def mock_admin(monkeypatch):
    """Mock admin 身分，繞過真實身分查詢"""
    monkeypatch.setattr(user_service, "get_user_role", lambda user_id: {"user_id": user_id, "role": "admin"})

@pytest.fixture
def mock_no_user(monkeypatch):
    from line_bot.services import user_service
    monkeypatch.setattr(user_service, "get_user_role", lambda user_id: None)

# autouse=True 全域pytest套用相同的設定
@pytest.fixture(autouse=True)
def set_mock_password():
    os.environ["PASSWORD_ADMIN"] = "1234"

@pytest.fixture(autouse=True)
def mock_env(monkeypatch, mock_line_api):
    monkeypatch.setattr(environment, "get_line_api", lambda: mock_line_api)
    monkeypatch.setattr(environment, "get_pinecone_index", lambda: "mock_index")
    monkeypatch.setattr(environment, "get_namespace", lambda: "mock-namespace")

# 假身分
