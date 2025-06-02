# services/postback_service.py

from config.role_config import ROLE_TEXT_MAP
from linebot.v3.messaging import TextMessage, ReplyMessageRequest
from adapters.auth_state_adapter import auth_store

class PostbackService:
    def __init__(self, user_id, data, line_bot_api, event):
        self.user_id = user_id
        self.data = data
        self.api = line_bot_api
        self.event = event

    def process(self):
        if self.data.startswith("role:"):
            self._handle_role_selection()

    def _handle_role_selection(self):
        role = self.data.split(":")[1]
        auth_store.set_pending_role(self.user_id, role)
        msg = f"🔐 請輸入 {ROLE_TEXT_MAP.get(role, role)} 的密碼"
        self._reply(msg)

    def _reply(self, text):
        self.api.reply_message(
            ReplyMessageRequest(
                reply_token=self.event.reply_token,
                messages=[TextMessage(text=text)]
            )
        )
