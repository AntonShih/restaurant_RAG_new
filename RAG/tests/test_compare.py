# from unittest.mock import MagicMock
# from RAG.core.compare import search_similar_faqs

# 測試指令 全域 $env:PYTHONPATH="."; poetry run pytest
# $env:PYTHONPATH="." ; poetry run pytest RAG/tests 
# $env:PYTHONPATH="." ; poetry run pytest RAG/tests/test_compare.py


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


from unittest.mock import patch, MagicMock

def test_search_similar_faqs_returns_results():
    mock_index = MagicMock()
    mock_index.query.return_value = {
        "matches": [
            {
                "metadata": {"question": "何時倒垃圾？", "answer": "晚上十點前倒垃圾"},
                "score": 0.95
            }
        ]
    }

    with patch("RAG.core.compare.embeddings.create") as mock_create:
        # ✅ 不要再寫 dict，要回傳一個真正有 .data 的物件
        mock_embedding = MagicMock()
        mock_embedding.embedding = [0.1] * 1536

        mock_response = MagicMock()
        mock_response.data = [mock_embedding]

        mock_create.return_value = mock_response
        
        from RAG.core import compare
        namespace = "test"
        query = "什麼時候要倒垃圾？"
        results = compare.search_similar_faqs(query, mock_index, namespace, top_k=3)

        assert isinstance(results, list)
        assert results[0]["metadata"]["question"] == "何時倒垃圾？"


