# from config.pinecone import get_pinecone_client
# import os
# from dotenv import load_dotenv
# load_dotenv()

# def get_pinecone_index(index_name: str = None):
#     """
#     取得 Pinecone Index 實例。

#     此函式會從環境變數取得預設的 index 名稱，
#     並使用已初始化的 Pinecone client 回傳對應的 Index 物件。

#     參數:
#         index_name (str): 可選。若提供則使用指定 index，否則預設從環境變數讀取。

#     回傳:
#         pinecone.Index: 指定名稱的 Pinecone Index 實例。
#     """
#     pc = get_pinecone_client()
#     index_name = index_name or os.getenv("PINECONE_INDEX_NAME")
#     return pc.Index(index_name)


# def query_index(vector, top_k=3, namespace=None):
#     """
#     查詢與輸入向量最相似的資料點。

#     使用 Pinecone 的向量查詢功能，根據指定的 index 與 namespace，
#     回傳與輸入向量最相近的 top_k 筆資料（含 metadata）。

#     參數:
#         vector (List[float]): 欲查詢的向量。
#         top_k (int): 要取回的相似結果數量，預設為 3。
#         namespace (str): 使用的 Pinecone 命名空間；若未指定則讀取環境變數預設值。

#     回傳:
#         List[Dict]: 查詢結果清單，每筆包含分數與 metadata。
#     """
#     index = get_pinecone_index()
#     namespace = namespace or os.getenv("PINECONE_NAMESPACE", "default")
#     return index.query(
#         vector=vector,
#         top_k=top_k,
#         include_metadata=True,
#         namespace=namespace
#     )


# adapters/pinecone_adapter.py

from config.pinecone import get_pinecone_client
import os

def get_pinecone_index(index_name: str = None):
    """
    取得 Pinecone Index 實例
    """
    pc = get_pinecone_client()
    index_name = index_name or os.getenv("PINECONE_INDEX_NAME")
    return pc.Index(index_name)

def query_index(vector, top_k=3, namespace=None):
    """
    封裝查詢邏輯，呼叫 Pinecone 查找相似向量
    """
    index = get_pinecone_index()
    namespace = namespace or os.getenv("PINECONE_NAMESPACE", "default")
    return index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )

def filter_matches_by_role(matches, access_level: int):
    """
    根據使用者權限篩選匹配結果
    """
    return [
        m for m in matches
        if int(m['metadata'].get("access_level")) <= access_level
    ]
