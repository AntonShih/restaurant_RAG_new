# conftest.py 是 pytest 的「自動加載設定檔」，可以用來定義所有測試都會用到的設定、資料夾初始化、fixture。
# from dotenv import load_dotenv

# load_dotenv()

import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture(autouse=True)
def mock_openai_embeddings():
    # 模擬整個 embeddings 模組（新版 SDK 的建議方式）
    fake_embeddings = MagicMock()
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1] * 1536)]
    fake_embeddings.create.return_value = mock_response

    # patch 整個 embeddings 屬性，而非 .create
    with patch("RAG.core.embedding.openai.embeddings", fake_embeddings), \
         patch("RAG.core.compare.openai.embeddings", fake_embeddings):
        yield
