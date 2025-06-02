import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

_pc = None

def init_pinecone():
    """初始化一次，不回傳，只管設好 _pc"""
    global _pc
    if _pc is None:
        _pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def get_pinecone_client():
    """負責回傳可安全使用的 _pc"""
    global _pc
    if _pc is None:
        raise RuntimeError("❌ 請先呼叫 init_pinecone()")
    return _pc


# def get_pinecone_index(index_name: str = None):
#     """取得 Pinecone Index 實例"""
#     if _pc is None:
#         raise RuntimeError("❌ 請先呼叫 init_pinecone()")
#     index_name = index_name or os.getenv("PINECONE_INDEX_NAME")
#     return _pc.Index(index_name)

def get_namespace():
    """取得 namespace（可供上傳與查詢共用）"""
    return os.getenv("PINECONE_NAMESPACE", "default")
