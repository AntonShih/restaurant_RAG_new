
from datetime import datetime, timezone

from line_bot.db.mongodb import get_db
from line_bot.config.role_config import ROLE_ACCESS_LEVEL, ROLE_TEXT_MAP

def save_user_role(user_id, role, from_liff=False):
    """儲存使用者身份與權限資訊"""
    users_collection = get_db()["user_roles"]

    user_data = {
        "user_id": user_id,
        "role": role,
        "role_text": ROLE_TEXT_MAP.get(role, role),
        "access_level": ROLE_ACCESS_LEVEL.get(role, 0),
        "verified_at": datetime.now(timezone.utc),
        "from_liff": from_liff,
        "updated_at": datetime.now(timezone.utc),
    }

    result = users_collection.update_one(
        {"user_id": user_id},
        {"$set": user_data},
        upsert=True
    )
    return result.acknowledged

def get_user_role(user_id):
    """根據 user_id 查詢該使用者身份資訊"""
    users_collection = get_db()["user_roles"]
    return users_collection.find_one({"user_id": user_id})

def init_user_roles_index():
    """建立唯一索引，加速查詢"""
    users_collection = get_db()["user_roles"]
    users_collection.create_index("user_id", unique=True)
# ---------------------------------------------------------------------------

# from datetime import datetime, timezone
# from line_bot.db.mongodb import get_db
# from line_bot.config.role_config import ROLE_ACCESS_LEVEL, ROLE_TEXT_MAP

# async def save_user_role(user_id, role, from_liff=False):
#     """非同步儲存使用者身份與權限資訊"""
#     users_collection = get_db()["user_roles"]

#     user_data = {
#         "user_id": user_id,
#         "role": role,
#         "role_text": ROLE_TEXT_MAP.get(role, role),
#         "access_level": ROLE_ACCESS_LEVEL.get(role, 0),
#         "verified_at": datetime.now(timezone.utc),
#         "from_liff": from_liff,
#         "updated_at": datetime.now(timezone.utc),
#     }

#     result = await users_collection.update_one(
#         {"user_id": user_id},
#         {"$set": user_data},
#         upsert=True
#     )
#     return result.acknowledged

# async def get_user_role(user_id):
#     """非同步查詢使用者身份資訊"""
#     users_collection = get_db()["user_roles"]
#     return await users_collection.find_one({"user_id": user_id})

# async def init_user_roles_index():
#     """非同步建立唯一索引"""
#     users_collection = get_db()["user_roles"]
#     await users_collection.create_index("user_id", unique=True)
