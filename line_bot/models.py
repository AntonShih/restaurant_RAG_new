# models.py

from line_bot.mongodb_client import get_db
from datetime import datetime

# 用戶集合
users_collection = get_db()["user_roles"]

# 角色等級映射，用於 RAG 系統權限控制
ROLE_ACCESS_LEVEL = {
    "normal": 1,
    "reserve": 2,
    "leader": 3,
    "vice_manager": 4,
    "manager": 5,
    "guest": 0
}

# SOP 類別對應可訪問的最低權限等級
SOP_CATEGORY_ACCESS = {
    "店務SOP": 1,
    "外場作業流程": 1,
    "內場操作流程": 1,
    "打烊與閉店流程": 1,
    "設備操作教學": 1,
    "突發狀況處理": 2,
    "客訴處理應對": 3,
    "外送與平台糾紛": 3,
    "退費與換餐規則": 3,
    "顧客心理與互動技巧": 2,
    "新人訓練指南": 3,
    "排班與請假制度": 4,
    "教育訓練與考核制度": 4,
    "人事與勞基法知識": 4,
    "定價與成本控制": 5,
    "品牌經營與價值觀": 4,
    "分店複製與拓點策略": 5,
    "促銷與行銷策略": 4,
    "人事隱性成本管理": 5,
    "法規與營運風險控管": 5
}

# 角色名稱對照表
ROLE_TEXT_MAP = {
    "normal": "一般職員",
    "reserve": "儲備幹部",
    "leader": "組長",
    "vice_manager": "副店長",
    "manager": "店長",
    "guest": "訪客"
}

def save_user_role(user_id, role, from_liff=False):
    user_data = {
        "user_id": user_id,
        "role": role,
        "role_text": ROLE_TEXT_MAP.get(role, role),
        "access_level": ROLE_ACCESS_LEVEL.get(role, 0),
        "verified_at": datetime.utcnow(),
        "from_liff": from_liff,
        "updated_at": datetime.utcnow()
    }
    result = users_collection.update_one(
        {"user_id": user_id},
        {"$set": user_data},
        upsert=True
    )
    return result.acknowledged

def get_user_role(user_id):
    return users_collection.find_one({"user_id": user_id})

def init_user_roles_index():
    users_collection.create_index("user_id", unique=True)

def load_sop_data():
    sop_collection = get_db()["sop"]
    count = sop_collection.count_documents({})
    if count == 0:
        print("SOP 資料不存在，正在初始化...")
        # 可加載初始 JSON 邏輯
    return sop_collection

def filter_sop_by_access_level(access_level):
    visible_categories = []
    for category, required_level in SOP_CATEGORY_ACCESS.items():
        if access_level >= required_level:
            visible_categories.append(category)
    return visible_categories

def query_sop_by_user(query, user_id):
    user = get_user_role(user_id)
    access_level = user.get("access_level", 0) if user else 0
    visible_categories = filter_sop_by_access_level(access_level)
    sop_collection = get_db()["sop"]
    results = list(sop_collection.find({
        "$and": [
            {"category": {"$in": visible_categories}},
            {"$or": [
                {"question": {"$regex": query, "$options": "i"}},
                {"answer": {"$regex": query, "$options": "i"}},
                {"category": {"$regex": query, "$options": "i"}}
            ]}
        ]
    }).limit(5))
    return results, visible_categories, access_level
