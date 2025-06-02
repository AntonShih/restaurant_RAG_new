import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from config.mongodb import get_mongodb_config

_client = None

def get_mongodb_client():
    """取得 MongoDB Client 實例（lazy singleton）"""
    global _client
    if _client is None:
        config = get_mongodb_config()
        print(f"🔧 MONGODB_URI = {config['uri']}")
        _client = MongoClient(
            config["uri"],
            server_api=ServerApi('1'),
            tlsCAFile=certifi.where()  # 加入憑證支援
        )
    return _client
        #  登入 MongoDB 主機
        #  使用 MONGODB_URI 做身分認證
        # 回傳一個 MongoClient 物件（代表連上主機）


def get_db():
    """取得指定資料庫實例"""
    config = get_mongodb_config()
    return get_mongodb_client()[config["db_name"]]
        # get_db():
        # 從 MongoClient 選出指定的資料庫（DB_NAME）
        # 回傳該資料庫（Database 物件）


def close_mongodb_client():
    """關閉 MongoDB client"""
    global _client
    if _client:
        _client.close()
        _client = None
