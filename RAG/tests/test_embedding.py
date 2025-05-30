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
from unittest.mock import patch
from RAG.core.embedding import embed_faq_list_batch

@patch("openai.embeddings.create")
def test_embed_faq_list_batch_generates_embedding(mock_create):
    mock_create.return_value = {
        "data": [{"embedding": [0.1] * 1536}]
    }

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
    assert len(result[0]["embedding"]) > 0
