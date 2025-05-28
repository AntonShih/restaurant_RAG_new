import os
from dotenv import load_dotenv
from pinecone import Pinecone
import openai
from linebot.v3.messaging import Configuration


# 讀取 .env 檔案內容進入 os.environ
load_dotenv()
_pc = None


def init_openai():
    """初始化 OpenAI"""
    openai.api_key = os.getenv("OPENAI_API_KEY")

def init_pinecone():
    """初始化 Pinecone Client（僅執行一次）"""
    global _pc
    if _pc is None:
        _pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def get_pinecone_index(index_name: str = None):
    """取得 Pinecone Index 實例"""
    if _pc is None:
        raise RuntimeError("❌ 請先呼叫 init_pinecone()")
    index_name = index_name or os.getenv("PINECONE_INDEX_NAME")
    return _pc.Index(index_name)

def get_namespace():
    """取得 namespace（可供上傳與查詢共用）"""
    return os.getenv("PINECONE_NAMESPACE", "default")

def get_line_configuration():
    """取得 LINE SDK 所需的設定物件"""
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    return Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)