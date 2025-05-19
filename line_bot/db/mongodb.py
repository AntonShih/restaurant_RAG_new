import os
import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# 載入 .env
load_dotenv()

# 檢查是否成功讀到 URI
print(f"🔧 MONGODB_URI = {os.getenv('MONGODB_URI')}")

# MongoDB 連接設定
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME", "linebot_db")

client = None

def get_mongodb_client():
    global client
    if client is None:
        client = MongoClient(
            MONGODB_URI,
            server_api=ServerApi('1'),
            tlsCAFile=certifi.where()  # 加入憑證支援
        )
    return client

def get_db():
    return get_mongodb_client()[DB_NAME]

def close_mongodb_client():
    global client
    if client:
        client.close()
        client = None
