# postback處理 對應動作
from config.role_config import ROLE_TEXT_MAP
from linebot.v3.messaging import TextMessage, FlexMessage
from adapters.auth_state_adapter import auth_store
from line_bot.templates.how_to_use import load_how_to_use_flex

class PostbackService:
    """
    處理來自 Rich Menu、按鈕等 postback 資料的服務類別
    """

    def __init__(self, user_id, data):
        self.user_id = user_id
        self.data = data

    def process(self):
        """
        主入口：根據 postback 資料內容決定處理邏輯，回傳一個 Message 物件
        """
        print(f"📨 收到 postback data：{self.data}")

        # 📘 使用說明卡片
        if self.data.startswith("action:how_to_use"):
            print("📘 使用說明卡片觸發")
            flex_content = load_how_to_use_flex()
            return FlexMessage(
                alt_text="📘 使用教學",
                contents=flex_content
            )

        # 🔐 選擇職位進行認證
        if self.data.startswith("role:"):
            return self._handle_role_selection()

    def _handle_role_selection(self):
        role = self.data.split(":")[1]
        auth_store.set_pending_role(self.user_id, role)
        msg = f"🔐 請輸入 {ROLE_TEXT_MAP.get(role, role)} 的密碼"
        return TextMessage(text=msg)
