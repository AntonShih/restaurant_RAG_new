# # 對應職位代碼的文字描述，例如 "manager" → "店長"
# from config.role_config import ROLE_TEXT_MAP

# # LINE Bot 所需的訊息格式
# from linebot.v3.messaging import TextMessage, ReplyMessageRequest

# # 封裝認證狀態的儲存與操作邏輯
# from adapters.auth_state_adapter import auth_store
# from line_bot1.handlers.postback_handler import handle_postback_usage

# class PostbackService:
#     """
#     處理來自 Rich Menu、按鈕等 postback 資料的服務類別
#     """

#     def __init__(self, user_id, data, line_bot_api, event):
#         # 儲存使用者與請求上下文
#         self.user_id = user_id
#         self.data = data
#         self.api = line_bot_api
#         self.event = event

#     def process(self):
#         """
#         主入口：根據 postback 資料內容決定處理邏輯
#         """
#         if self.data == "action:how_to_use":
#             print("📘 使用說明卡片觸發")
#             handle_postback_usage(self.event, self.api)
#             return
    
#         # 若 postback 是選擇角色的指令，例如 "role:manager"
#         if self.data.startswith("role:"):
#             self._handle_role_selection()

#     def _handle_role_selection(self):
#         """
#         當使用者從選單中選擇一個角色後，記錄該角色並要求輸入密碼
#         """
#         # 擷取角色代碼，例如 "role:manager" → "manager"
#         role = self.data.split(":")[1]

#         # 將該使用者的待驗證角色暫存起來，等待輸入密碼
#         auth_store.set_pending_role(self.user_id, role)

#         # 回覆訊息：提示使用者輸入對應角色的密碼
#         msg = f"🔐 請輸入 {ROLE_TEXT_MAP.get(role, role)} 的密碼"
#         self._reply(msg)

#     def _reply(self, text):
#         """
#         將文字訊息以 LINE Message API 的格式回覆給使用者
#         """
#         self.api.reply_message(
#             ReplyMessageRequest(
#                 reply_token=self.event.reply_token,
#                 messages=[TextMessage(text=text)]
#             )
#         )


# from config.role_config import ROLE_TEXT_MAP
# from linebot.v3.messaging import TextMessage, FlexMessage
# from adapters.auth_state_adapter import auth_store
# from linebot.v3.messaging.models.reply_message_request import ReplyMessageRequest
# from line_bot1.templates.how_to_use import load_flex_template

# class PostbackService:
#     """
#     處理來自 Rich Menu、按鈕等 postback 資料的服務類別
#     """

#     def __init__(self, user_id, data):
#         self.user_id = user_id
#         self.data = data

#     def process(self):
#         """
#         主入口：根據 postback 資料內容決定處理邏輯，回傳一個 Message 物件
#         """
#         print(f"📨 收到 postback data：{self.data}")
#         if self.data.startswith("action:how_to_use"):
#             print("📘 使用說明卡片觸發")
#             print("🧩 Flex 內容預覽：", json.dumps(how_to_use_flex["contents"], indent=2, ensure_ascii=False))

#             return FlexMessage(
#                 alt_text=how_to_use_flex["altText"],
#                 contents=FlexContainer.from_dict(how_to_use_flex["contents"])
#             )

#         if self.data.startswith("role:"):
#             return self._handle_role_selection()

#         # 預設回傳 None
#         return TextMessage(text="⚠️ 尚未支援的 postback 指令")

#     def _handle_role_selection(self):
#         role = self.data.split(":")[1]
#         auth_store.set_pending_role(self.user_id, role)
#         msg = f"🔐 請輸入 {ROLE_TEXT_MAP.get(role, role)} 的密碼"
#         return TextMessage(text=msg)

#     def handle_postback_how_to_use(event, line_bot_api):
#         flex_content = load_flex_template("line_bot1/templates/how_to_use_card.json")
#         message = FlexMessage(
#             alt_text="📘 使用教學",
#             contents=flex_content
#         )
#         line_bot_api.reply_message(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[message]
#             )
#         )

from config.role_config import ROLE_TEXT_MAP
from linebot.v3.messaging import TextMessage, FlexMessage
from adapters.auth_state_adapter import auth_store
from line_bot1.templates.how_to_use import load_how_to_use_flex

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

        # ❌ 未支援的 postback
        return TextMessage(text="⚠️ 尚未支援的 postback 指令")

    def _handle_role_selection(self):
        role = self.data.split(":")[1]
        auth_store.set_pending_role(self.user_id, role)
        msg = f"🔐 請輸入 {ROLE_TEXT_MAP.get(role, role)} 的密碼"
        return TextMessage(text=msg)
