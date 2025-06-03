# 對應職位代碼的文字描述，例如 "manager" → "店長"
from config.role_config import ROLE_TEXT_MAP

# LINE Bot 所需的訊息格式
from linebot.v3.messaging import TextMessage, ReplyMessageRequest

# 封裝認證狀態的儲存與操作邏輯
from adapters.auth_state_adapter import auth_store

class PostbackService:
    """
    處理來自 Rich Menu、按鈕等 postback 資料的服務類別
    """

    def __init__(self, user_id, data, line_bot_api, event):
        # 儲存使用者與請求上下文
        self.user_id = user_id
        self.data = data
        self.api = line_bot_api
        self.event = event

    def process(self):
        """
        主入口：根據 postback 資料內容決定處理邏輯
        """
        # 若 postback 是選擇角色的指令，例如 "role:manager"
        if self.data.startswith("role:"):
            self._handle_role_selection()

    def _handle_role_selection(self):
        """
        當使用者從選單中選擇一個角色後，記錄該角色並要求輸入密碼
        """
        # 擷取角色代碼，例如 "role:manager" → "manager"
        role = self.data.split(":")[1]

        # 將該使用者的待驗證角色暫存起來，等待輸入密碼
        auth_store.set_pending_role(self.user_id, role)

        # 回覆訊息：提示使用者輸入對應角色的密碼
        msg = f"🔐 請輸入 {ROLE_TEXT_MAP.get(role, role)} 的密碼"
        self._reply(msg)

    def _reply(self, text):
        """
        將文字訊息以 LINE Message API 的格式回覆給使用者
        """
        self.api.reply_message(
            ReplyMessageRequest(
                reply_token=self.event.reply_token,
                messages=[TextMessage(text=text)]
            )
        )

