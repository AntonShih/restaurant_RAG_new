# 暫存的list
pending_password_check = {}

# 暫存使用者
def start_auth(user_id, role):
    pending_password_check[user_id] = {"role": role, "attempts": 0}

# 刪除使用者在暫存
def complete_auth(user_id):
    pending_password_check.pop(user_id, None)

# 確認使用者是否在暫存，若是則開始驗證
def is_auth_pending(user_id):
    return user_id in pending_password_check

# 他想驗證什麼角色
def get_pending_role(user_id):
    return pending_password_check.get(user_id, {}).get("role")

# 計算驗證次數
def increment_attempt(user_id):
    if user_id in pending_password_check:
        pending_password_check[user_id]["attempts"] += 1
        return pending_password_check[user_id]["attempts"]
    return 0