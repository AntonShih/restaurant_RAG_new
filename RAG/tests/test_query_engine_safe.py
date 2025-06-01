# 測試指令 全域 $env:PYTHONPATH="."; poetry run pytest
# $env:PYTHONPATH="." ; poetry run pytest RAG/tests 
# $env:PYTHONPATH="." ; poetry run pytest RAG/tests/test_query_engine_safe.py
from unittest.mock import patch, MagicMock
from RAG.query.query_engine_safe import answer_query_secure


@patch("RAG.query.query_engine_safe.get_user_role")
@patch("RAG.query.query_engine_safe.search_similar_faqs")
@patch("RAG.query.query_engine_safe.openai.chat.completions.create")
def test_answer_query_secure_success(mock_create, mock_search, mock_get_user_role):
    # 假的 user（有權限）
    mock_get_user_role.return_value = {"user_id": "test_user", "access_level": 1}

    # 假的向量比對結果（其中一筆 access_level = 1）
    mock_search.return_value = [
        {
            "metadata": {
                "question": "What is Python?",
                "answer": "A programming language.",
                "access_level": 1
            },
            "score": 0.9
        }
    ]

    # 假的 GPT 回覆
    mock_create.return_value.choices = [
        MagicMock(message=MagicMock(content="Python 是一種程式語言。"))
    ]

    # 呼叫被測試函式
    fake_index = MagicMock()
    fake_namespace = "test"

    result = answer_query_secure("What is Python?", "test_user", fake_index, fake_namespace)

    assert "程式語言" in result


@patch("RAG.query.query_engine_safe.get_user_role")
@patch("RAG.query.query_engine_safe.search_similar_faqs")
def test_answer_query_secure_no_user(mock_search, mock_get_user_role):
    mock_get_user_role.return_value = None  # 查無此人
    mock_search.return_value = [
        {
            "metadata": {
                "question": "How to login?",
                "answer": "Use your credentials.",
                "access_level": 3  # 使用者沒權限
            },
            "score": 0.8
        }
    ]

    result = answer_query_secure("How to login?", "unknown_user", MagicMock(), "test")

    assert "職等無法查閱" in result

def test_answer_query_secure_no_results():
    with patch("RAG.query.query_engine_safe.get_user_role", return_value={"access_level": 1}), \
         patch("RAG.query.query_engine_safe.search_similar_faqs", return_value=[]):
        result = answer_query_secure("Empty test", "test_user", MagicMock(), "test")
        assert "查無相關 FAQ" in result or "職等無法查閱" in result
