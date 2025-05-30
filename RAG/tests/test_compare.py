# from unittest.mock import MagicMock
# from RAG.core.compare import search_similar_faqs

# # 測試指令 全域 $env:PYTHONPATH="."; poetry run pytest
# # $env:PYTHONPATH="." ; poetry run pytest RAG/tests 
# # $env:PYTHONPATH="." ; poetry run pytest RAG/tests/test_compare.py 


# def test_search_similar_faqs_returns_results():
#     mock_index = MagicMock()
#     mock_index.query.return_value = {
#         "matches": [
#             {
#                 "metadata": {"question": "何時倒垃圾？", "answer": "晚上十點前倒垃圾"},
#                 "score": 0.95
#             }
#         ]
#     }
#     namespace = "test"
#     query = "什麼時候要倒垃圾？"

#     results = search_similar_faqs(query, mock_index, namespace, top_k=3)

#     assert isinstance(results, list)
#     assert len(results) > 0
#     assert "metadata" in results[0]
#     assert "question" in results[0]["metadata"]
#     assert "answer" in results[0]["metadata"]


from unittest.mock import MagicMock, patch
from RAG.core.compare import search_similar_faqs

@patch("openai.embeddings.create")
def test_search_similar_faqs_returns_results(mock_create):
    # Mock OpenAI embeddings.create
    mock_create.return_value = {
        "data": [{"embedding": [0.1] * 1536}]
    }

    mock_index = MagicMock()
    mock_index.query.return_value = {
        "matches": [
            {
                "metadata": {"question": "何時倒垃圾？", "answer": "晚上十點前倒垃圾"},
                "score": 0.95
            }
        ]
    }
    namespace = "test"
    query = "什麼時候要倒垃圾？"

    results = search_similar_faqs(query, mock_index, namespace, top_k=3)

    assert isinstance(results, list)
    assert len(results) > 0
    assert "metadata" in results[0]
    assert "question" in results[0]["metadata"]
    assert "answer" in results[0]["metadata"]
