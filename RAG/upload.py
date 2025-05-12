def format_for_pinecone(faq_list: list) -> list:
    pinecone_vectors = []
    for i, faq in enumerate(faq_list):
        vector = {
            "id": f"faq_{i+1}",
            "values": faq["embedding"],
            "metadata": {
                "question": faq["question"],
                "answer": faq["answer"],
                "category": faq.get("category", ""),
                "access_level": faq.get("access_level", 1)  # 添加權限等級到元數據
            }
        }
        pinecone_vectors.append(vector)
    return pinecone_vectors
