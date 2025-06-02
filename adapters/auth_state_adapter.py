# adapters/auth_state_adapter.py

class AuthStateStore:
    def __init__(self):
        # 使用者暫存的角色資料（尚未完成認證的角色）
        # 結構：{user_id: role}
        self._pending_roles = {}

        # 使用者輸入密碼的次數記錄（限制最多3次）
        # 結構：{user_id: attempt_count}
        self._auth_attempts = {}

    def set_pending_role(self, user_id, role):
        """
        設定使用者正在進行認證的角色，同時初始化錯誤次數為 0。
        """
        self._pending_roles[user_id] = role
        self._auth_attempts[user_id] = 0

    def get_pending_role(self, user_id):
        """
        取得尚未完成認證的使用者角色。
        若使用者不在暫存中，回傳 None。
        """
        return self._pending_roles.get(user_id)

    def clear_pending(self, user_id):
        """
        清除使用者的暫存角色與輸入錯誤次數（完成認證或達到錯誤次數上限時使用）。
        """
        self._pending_roles.pop(user_id, None)
        self._auth_attempts.pop(user_id, None)

    def increment_attempt(self, user_id):
        """
        增加使用者的錯誤嘗試次數，回傳更新後的次數。
        若是第一次呼叫，預設從 0 開始。
        """
        self._auth_attempts[user_id] = self._auth_attempts.get(user_id, 0) + 1
        return self._auth_attempts[user_id]

    def get_attempts(self, user_id):
        """
        回傳使用者目前累積的錯誤次數，若未記錄則回傳 0。
        """
        return self._auth_attempts.get(user_id, 0)


# 全域單例，供整個系統共用一份認證暫存狀態
auth_store = AuthStateStore()
