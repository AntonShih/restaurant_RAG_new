# RAG/tests/conftest.py

import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture(autouse=True)
def mock_openai_embedding():
    # ✅ patch 兩個地方：embedding.py、compare.py 中的 openai.embeddings.create
    with patch("RAG.core.embedding.openai.embeddings.create") as mock_create_embed, \
         patch("RAG.core.compare.openai.embeddings.create") as mock_create_compare:

        # 建立假的回傳值
        mock_embedding = MagicMock()
        mock_embedding.embedding = [0.1] * 1536

        mock_response = MagicMock()
        mock_response.data = [mock_embedding]

        # 設定回傳值
        mock_create_embed.return_value = mock_response
        mock_create_compare.return_value = mock_response

        yield  # ✅ mock 會在每個 test 開始時自動套用
