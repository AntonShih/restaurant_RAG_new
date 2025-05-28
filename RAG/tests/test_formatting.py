from RAG.core.formatting import format_for_pinecone

def test_format_for_pinecone_basic():
    sample_faqs = [
        {
            "question": "什麼時候要倒垃圾？",
            "answer": "每日 22:30 前",
            "category": "SOP",
            "access_level": "staff",
            "embedding": [0.1, 0.2, 0.3]
        },
        {
            "question": "刷地什麼時候做？",
            "answer": "閉店後",
            "category": "SOP",
            "access_level": "manager",
            "embedding": [0.4, 0.5, 0.6]
        }
    ]

    result = format_for_pinecone(sample_faqs)

    assert isinstance(result, list)
    assert len(result) == 2

    for i, vec in enumerate(result):
        assert vec["id"] == f"faq_{i+1}"
        assert vec["values"] == sample_faqs[i]["embedding"]
        assert vec["metadata"]["question"] == sample_faqs[i]["question"]
        assert vec["metadata"]["answer"] == sample_faqs[i]["answer"]
        assert vec["metadata"]["category"] == sample_faqs[i]["category"]
        assert vec["metadata"]["access_level"] == sample_faqs[i]["access_level"]
