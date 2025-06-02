
# adapters/user_role_adapter.py

from datetime import datetime, timezone
from config.role_config import ROLE_ACCESS_LEVEL, ROLE_TEXT_MAP
from line_bot.db.mongodb import get_db

user_role_collection = get_db()["user_role"]

def save_user_role(user_id: str, role: str):
    """
    儲存使用者角色資訊，若已存在則更新。
    包含角色名稱、中文名稱、權限等級、驗證時間。
    """
    user_data = {
        "role": role,
        "role_text": ROLE_TEXT_MAP.get(role, role),
        "access_level": ROLE_ACCESS_LEVEL.get(role, 0),
        "verified_at": datetime.now(timezone.utc)
    }

    user_role_collection.update_one(
        {"user_id": user_id},
        {"$set": user_data},
        upsert=True
    )

def get_user_role(user_id: str) -> dict | None:
    """
    取得完整的使用者角色資訊（若無資料則回傳 None）
    回傳內容範例：
    {
        "user_id": "xxx",
        "role": "staff",
        "role_text": "內場人員",
        "access_level": 2,
        ...
    }
    """
    return user_role_collection.find_one({"user_id": user_id})
