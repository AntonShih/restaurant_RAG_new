from config.pinecone import get_pinecone_client
import os

def get_pinecone_index(index_name: str = None):
    """
    取得 Pinecone Index 實例。
    
    若未傳入 index_name，則從環境變數 PINECONE_INDEX_NAME 讀取。
    用於後續查詢或上傳向量的操作。
    """
    pc = get_pinecone_client()
    index_name = os.getenv("PINECONE_INDEX_NAME")
    return pc.Index(index_name)

def query_index(vector, top_k=3, namespace=None):
    """
    呼叫 Pinecone 向量資料庫查詢相似向量。

    參數：
    - vector: 欲查詢的向量
    - top_k: 回傳最相似的前幾筆
    - namespace: 分區名稱（可分開儲存不同資料集）

    回傳：
    - 查詢結果字典，包含匹配項目與 metadata
    """
    index = get_pinecone_index()
    namespace = os.getenv("PINECONE_NAMESPACE")
    return index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )

def filter_matches_by_role(matches, access_level: int):
    """
    根據使用者的 access_level 權限，篩選查詢結果中可以看的項目。

    參數：
    - matches: Pinecone 查詢回傳的 matches 列表
    - access_level: 使用者權限（數字越大權限越高）

    回傳：
    - 篩選後使用者有權限查看的 matches
    """
    return [
        m for m in matches
        if int(m['metadata'].get("access_level")) <= access_level
    ]
