from openai import embeddings
from typing import List

def search_similar_faqs(query: str, index, namespace: str, top_k: int = 3)-> List[dict]:
    """
    根據輸入的問題 query，使用 OpenAI 嵌入後查詢 Pinecone 資料庫中最相似的 FAQ。

    參數:
        query (str): 使用者輸入的問題句子。
        index: 已初始化的 Pinecone Index 物件。
        namespace (str): Pinecone namespace，用於區分資料區。
        top_k (int): 回傳相似度最高的前 k 筆資料，預設為 3。

    回傳:
        List[dict] - 每筆資料包含 metadata 及相似度。
    """
    ...
    
    response = embeddings.create(
        input=query,
        model="text-embedding-3-small"
    )
    query_vector = response.data[0].embedding

    result = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )
    return result["matches"]
