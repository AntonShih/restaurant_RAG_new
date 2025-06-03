
from typing import List

def compare_vectors(query_vector, index, namespace: str, top_k: int = 3) -> List[dict]:
    """
    負責根據使用者輸入的 query 向量在向量索引庫中查詢最相近的資料。

    模組歸屬說明：
    - 此函式屬於「核心商業邏輯」，即『如何比對語意向量』，而非連接 Pinecone 或處理輸入輸出的細節。
    - 不負責初始化 index 也不處理網路連線，這些應該在 adapters 或 config 中處理。
    - 雖然呼叫了 index.query()，但 index 被當作參數傳入，這代表它對外部套件無直接耦合，因此可以被重複利用、單元測試與替換。

    適合放在 core 的原因：
    - 涉及的是「應用邏輯層Application Logic」:比對、排序、取前 K 筆資料。
    - 不依賴具體實作（像是 Pinecone、FAISS、Qdrant 都可以傳進來作為 index)。
    - 提供一個可以被 service 或 controller 呼叫的核心功能單位。

    參數：
    - index:外部傳入的向量資料庫索引物件（例如 Pinecone 的 Index 實例）
    - namespace:使用哪個命名空間的資料（用來隔離不同用途的資料）

    回傳：
    - List[dict]：每筆資料為一個 dict，包含 match 的 id、score 和 metadata(如原始問題、access_level 等）
    """
    return index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )["matches"]

# # {
#   "id": "faq123",
#   "score": 0.92,
#   "metadata": {
#     "question": "你有沒有提供外帶？",
#     "access_level": 1
#   }
# }