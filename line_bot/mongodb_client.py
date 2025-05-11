import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB 連接設定
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME", "linebot_db")

# MongoDB 連接客戶端
client = None

def get_mongodb_client():
    """獲取 MongoDB 客戶端連接"""
    global client
    if client is None:
        client = MongoClient(MONGODB_URI)
    return client

def get_db():
    """獲取資料庫物件"""
    return get_mongodb_client()[DB_NAME]

def close_mongodb_client():
    """關閉 MongoDB 連接"""
    global client
    if client:
        client.close()
        client = None