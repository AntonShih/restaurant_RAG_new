pending_password_check = {}

def start_auth(user_id, role):
    pending_password_check[user_id] = {"role": role, "attempts": 0}

def complete_auth(user_id):
    pending_password_check.pop(user_id, None)

def is_auth_pending(user_id):
    return user_id in pending_password_check

def get_pending_role(user_id):
    return pending_password_check.get(user_id, {}).get("role")

def increment_attempt(user_id):
    if user_id in pending_password_check:
        pending_password_check[user_id]["attempts"] += 1
        return pending_password_check[user_id]["attempts"]
    return 0