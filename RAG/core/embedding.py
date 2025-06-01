import openai


def embed_faq_list_batch(faq_list):
    result = []
    for item in faq_list:
        response = openai.embeddings.create(
            input=item["question"],
            model="text-embedding-3-small"
        )
        item["embedding"] = response.data[0].embedding
        result.append(item)
    return result


# [
#     {
#         "question": "如何清洗咖啡機？",
#         "answer": "請於營業結束後依照清潔 SOP 進行清洗。",
#         "category": "設備操作",
#         "embedding": [0.013, -0.027, 0.054, ..., 0.008]  # ⬅️ 長度為 1536 的浮點數列表
#     },
#     {
#         "question": "員工請假需要幾天前申請？",
#         "answer": "需於三天前提出申請。",
#         "category": "人事制度",
#         "embedding": [0.001, 0.007, -0.009, ..., -0.002]
#     }
# ]
