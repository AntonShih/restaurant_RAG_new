
from line_bot.db.mongodb import get_db
from line_bot.services.user_service import get_user_role

def query_sop_by_user(query: str, user_id: str):
    """根據使用者的 access_level，查詢符合權限的 SOP 問答"""
    user = get_user_role(user_id)
    access_level = user.get("access_level",0) if user else 0

    sop_collection = get_db()["sop"]

    results = list(sop_collection.find({
        "access_level": {"$lte": access_level},
        "$or": [
            {"question": {"$regex": query, "$options": "i"}},
            {"answer": {"$regex": query, "$options": "i"}},
            {"category": {"$regex": query, "$options": "i"}}
        ]
    }).limit(5))

    return results, access_level
