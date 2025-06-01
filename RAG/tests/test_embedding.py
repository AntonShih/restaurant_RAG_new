# from RAG.core.embedding import embed_faq_list_batch

# def test_embed_faq_list_batch_generates_embedding():
#     # 模擬一筆 FAQ
#     sample_data = [
#         {
#             "question": "如何清洗咖啡機？",
#             "answer": "請於營業結束後依照清潔 SOP 進行清洗。",
#             "category": "設備操作"
#         }
#     ]

#     result = embed_faq_list_batch(sample_data)

#     assert isinstance(result, list)
#     assert "embedding" in result[0]
#     assert isinstance(result[0]["embedding"], list)
#     assert len(result[0]["embedding"]) > 0

# 測試指令 全域 $env:PYTHONPATH="."; poetry run pytest
# $env:PYTHONPATH="." ; poetry run pytest RAG/tests 
# $env:PYTHONPATH="." ; poetry run pytest RAG/tests/test_embedding.py
# ----------------------------------------------------------
# from unittest.mock import patch, MagicMock

# @patch("RAG.core.embedding.openai.embeddings.create")
# def test_embed_faq_list_batch_generates_embedding(mock_create):
#     # 模擬回傳的 embedding 格式
#     mock_embedding = MagicMock()
#     mock_embedding.embedding = [0.1] * 1536

#     mock_response = MagicMock()
#     mock_response.data = [mock_embedding]

#     mock_create.return_value = mock_response
    
#     from RAG.core.embedding import embed_faq_list_batch
#     sample_data = [
#         {
#             "question": "如何清洗咖啡機？",
#             "answer": "請於營業結束後依照清潔 SOP 進行清洗。",
#             "category": "設備操作"
#         }
#     ]

#     result = embed_faq_list_batch(sample_data)

#     assert isinstance(result, list)
#     assert "embedding" in result[0]
#     assert isinstance(result[0]["embedding"], list)
#     assert len(result[0]["embedding"]) == 1536
# -------------------------------------------------------
from RAG.core.embedding import embed_faq_list_batch

def test_embed_faq_list_batch_generates_embedding():
    sample_data = [
        {
            "question": "如何清洗咖啡機？",
            "answer": "請於營業結束後依照清潔 SOP 進行清洗。",
            "category": "設備操作"
        }
    ]

    result = embed_faq_list_batch(sample_data)

    assert isinstance(result, list)
    assert "embedding" in result[0]
    assert isinstance(result[0]["embedding"], list)
    assert len(result[0]["embedding"]) == 1536
