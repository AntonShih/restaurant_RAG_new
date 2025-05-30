import os
import pytest
from config import environment

@pytest.fixture
def mock_line_api():
    class MockLineAPI:
        def __init__(self): self.replies = []
        def reply_message(self, request):
            self.replies.append([m.text for m in request.messages])
    return MockLineAPI()

# autouse=True 全域pytest套用相同的設定
@pytest.fixture(autouse=True)
def set_mock_password():
    os.environ["PASSWORD_ADMIN"] = "1234"

@pytest.fixture(autouse=True)
def mock_env(monkeypatch, mock_line_api):
    monkeypatch.setattr(environment, "get_line_api", lambda: mock_line_api)
    monkeypatch.setattr(environment, "get_pinecone_index", lambda: "mock_index")
    monkeypatch.setattr(environment, "get_namespace", lambda: "mock-namespace")
