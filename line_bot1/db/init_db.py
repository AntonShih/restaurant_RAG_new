# line_bot/db/init_db.py

from line_bot1.db.mongodb import get_db

def init_user_roles_index():
    """確保 user_role 集合存在 user_id 的唯一索引"""
    collection = get_db()["user_role"]
    collection.create_index("user_id", unique=True)
