from datetime import datetime
from mongodb_client import get_db

# 用戶集合
users_collection = get_db()["users"]

# 角色等級映射，用於 RAG 系統權限控制
ROLE_ACCESS_LEVEL = {
    "kitchen": 1,
    "front": 1,
    "reserve": 2,
    "leader": 3,
    "vice_manager": 4,
    "manager": 5
}

def save_user_role(user_id, role):
    """儲存或更新用戶角色"""
    user_data = {
        "user_id": user_id,
        "role": role,
        "role_text": role_text_map.get(role, role),
        "access_level": ROLE_ACCESS_LEVEL.get(role, 0),
        "updated_at": datetime.now()
    }
    
    # 使用 upsert 功能，不存在則建立，存在則更新
    result = users_collection.update_one(
        {"user_id": user_id},
        {"$set": user_data},
        upsert=True
    )
    
    return result.acknowledged

def get_user_role(user_id):
    """獲取用戶角色信息"""
    user = users_collection.find_one({"user_id": user_id})
    return user if user else None