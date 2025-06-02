# services/auth_service.py
from adapters.auth_state_adapter import auth_store
from config.role_config import ROLE_KEY_MAP, ROLE_TEXT_MAP
from core.auth.password import verify_password
from adapters.user_role_adapter import save_user_role  
from linebot.v3.messaging import TextMessage, ReplyMessageRequest
import os

class AuthService:
    def __init__(self, user_id, text, line_bot_api, event):
        self.user_id = user_id
        self.text = text
        self.api = line_bot_api
        self.event = event

    def process(self) -> bool:
        """統一處理認證流程"""
        if self._handle_identity_input():
            return True
        if auth_store.get_pending_role(self.user_id):
            self._handle_password_input()
            return True
        return False

    def _handle_identity_input(self) -> bool:
        """處理『認證：角色』輸入，寫入暫存"""
        if self.text.startswith("認證："):
            role_input = self.text.replace("認證：", "").strip()
            role = ROLE_KEY_MAP.get(role_input, role_input)
            auth_store.set_pending_role(self.user_id, role)

            self._reply(f"🔐 請輸入 {ROLE_TEXT_MAP.get(role, role)} 的密碼")
            return True
        return False

    def _handle_password_input(self):
        """處理密碼驗證邏輯與回應"""
        role = auth_store.get_pending_role(self.user_id)
        expected = os.getenv(f"PASSWORD_{role.upper()}")

        if verify_password(expected, self.text):
            save_user_role(self.user_id, role)
            auth_store.clear_pending(self.user_id)
            msg = f"密碼正確，您已成功認證為：{ROLE_TEXT_MAP.get(role, role)}"
        else:
            attempts = auth_store.increment_attempt(self.user_id)
            if attempts >= 3:
                auth_store.clear_pending(self.user_id)
                msg = "❌ 已連續輸入錯誤 3 次，已轉為 QA 模式。"
            else:
                remaining = 3 - attempts
                msg = f"❌ 密碼錯誤，請重新輸入。您還有 {remaining} 次機會"

        self._reply(msg)

    def _reply(self, text):
        """簡化回應封裝邏輯"""
        self.api.reply_message(
            ReplyMessageRequest(
                reply_token=self.event.reply_token,
                messages=[TextMessage(text=text)]
            )
        )

