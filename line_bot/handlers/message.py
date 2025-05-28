# from linebot.v3.webhooks import MessageEvent, TextMessageContent
# from linebot.v3.messaging import (
#     Configuration, ApiClient, MessagingApi,
#     ReplyMessageRequest, TextMessage
# )
# import os

# from line_bot.services.user_service import save_user_role, get_user_role
# from line_bot.services.auth_state import (
#     start_auth, complete_auth, is_auth_pending,
#     get_pending_role, increment_attempt
# )
# from line_bot.config.role_config import ROLE_TEXT_MAP
# from RAG.query.query_engine_safe import answer_query_secure
# from config.environment import init_openai, get_pinecone_index, get_namespace, init_pinecone

# # 初始化 LINE Bot 設定 身份憑證
# LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
# configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)

# # === 驗證密碼暫時擺在這，未來可以獨立封裝 ===
# def verify_password(role: str, password: str) -> bool:
#     expected = os.getenv(f"PASSWORD_{role.upper()}")
#     return password == expected

# def handle_message(event: MessageEvent):

#     # 初始化 Pinecone 與 OpenAI（可放主程式只跑一次）
#     init_openai()
#     init_pinecone()

#     # 拿到 index 與 namespace
#     index = get_pinecone_index()
#     namespace = get_namespace()

#     user_id = event.source.user_id
#     text = event.message.text.strip()

#     # 跟 LINE 官方伺服器的連線對象
#     with ApiClient(configuration) as api_client:
#         # INE Bot 的功能菜單
#         line_bot_api = MessagingApi(api_client)

#             # Step 1：身份認證流程
#         if text.startswith("認證："):
#             role = text.replace("認證：", "").strip()
#             start_auth(user_id, role)  # 暫存角色、驗證次數
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[TextMessage(text=f"🔐 請輸入 {ROLE_TEXT_MAP.get(role, role)} 的密碼")]
#                 )
#             )
#             return

#         # Step 2：密碼驗證 暫存的認證流程記憶體（未正式存檔），如果使用者在這裡pending_password_check就代表他想驗證
#         if is_auth_pending(user_id):  # 看是不是想驗證
#             role = get_pending_role(user_id)  # 驗證啥角色

#             if verify_password(role, text):
#                 save_user_role(user_id, role)
#                 complete_auth(user_id)  #  成功後移除
#                 line_bot_api.reply_message(
#                     ReplyMessageRequest(
#                         reply_token=event.reply_token,
#                         messages=[TextMessage(text=f"密碼正確，您已成功認證為：{ROLE_TEXT_MAP.get(role, role)}")]
#                     )
#                 )
#                 return
#             else:
#                 attempts = increment_attempt(user_id)  # 嘗試次數封裝
#                 remaining = 3 - attempts

#                 if attempts >= 3:
#                     complete_auth(user_id)  # 清除失敗者
#                     line_bot_api.reply_message(
#                         ReplyMessageRequest(
#                             reply_token=event.reply_token,
#                             messages=[TextMessage(text="❌ 已連續輸入錯誤 3 次，已幫您轉換為QA回答模式。若想請重新驗證請選擇角色。")]
#                         )
#                     )
#                     return
#                 else:
#                     line_bot_api.reply_message(
#                         ReplyMessageRequest(
#                             reply_token=event.reply_token,
#                             messages=[TextMessage(text=f"❌ 密碼錯誤，請重新輸入。您還有 {remaining} 次機會")]
#                         )
#                     )
#                     return
#         # 進入 RAG 查詢流程（Step 3）已寫入 DB 的正式身份資訊，如果使用者不在pending_password_check就代表想找東西
#         user = get_user_role(user_id) #雖然他回傳詳細資料但我只用來看有沒有驗證成功而已
#         if user:
#             try:
#                 rag_answer = answer_query_secure(text, user_id, index, namespace)
#             except Exception as e:
#                 print("❌ RAG 查詢失敗：", str(e))
#                 rag_answer = "❌ 回答時發生錯誤，請稍後再試。"
#         else:
#             rag_answer = "⚠️ 查無使用者身份資訊，請先完成認證。"

#         line_bot_api.reply_message(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=rag_answer)]
#             )
#         )
#         return
        
# ---------------------------------------------------------------------------------------------------
# 用來處理message event後的邏輯  
# 1.是否輸入驗"證試:"了畫會直接接著跑2.
# 2.從暫存中抓帳號在裡面的就是要認證 認證制度是3次 postback 因為會暫存也被丟過來
# 3.都不是就直接取得mongo user role 進行RAG

from linebot.v3.webhooks import MessageEvent
from linebot.v3.messaging import ReplyMessageRequest, TextMessage
from config.environment import (
    init_openai, init_pinecone,
    get_pinecone_index, get_namespace,
    get_line_api
)
from line_bot.services.user_service import save_user_role, get_user_role
from line_bot.services.auth_state import (
    start_auth, complete_auth, is_auth_pending,
    get_pending_role, increment_attempt
)
from line_bot.config.role_config import ROLE_TEXT_MAP,ROLE_KEY_MAP
from RAG.query.query_engine_safe import answer_query_secure


def handle_message(event: MessageEvent):
    """
    訊息處理主流程 
    1.是否輸入驗"證試:"了畫會直接接著跑2.
    2.從暫存中抓帳號在裡面的就是要認證 認證制度是3次 postback 因為會暫存也被丟過來
    3.都不是就直接取得mongo user role 進行RAG
    """
    init_openai()
    init_pinecone()
    index = get_pinecone_index()
    namespace = get_namespace()
    user_id = event.source.user_id
    text = event.message.text.strip()

    line_bot_api = get_line_api()

    if handle_identity_auth_flow(text, user_id, line_bot_api, event):
            return

    if is_auth_pending(user_id):
            handle_pending_password_flow(text, user_id, line_bot_api, event)
            return

    handle_rag_flow(text, user_id, index, namespace, line_bot_api, event)


def handle_identity_auth_flow(text, user_id, line_bot_api, event) -> bool:
    """是否輸入驗證:是了化把使加入暫存"""
    if text.startswith("認證："):
        role_input = text.replace("認證：", "").strip()
        role = ROLE_KEY_MAP.get(role_input, role_input)  # 中文也支援

        start_auth(user_id, role)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=f"🔐 請輸入 {ROLE_TEXT_MAP.get(role, role)} 的密碼")]
            )
        )
        return True
    return False


def handle_pending_password_flow(text, user_id, line_bot_api, event):
    """從暫存中抓帳號在裡面的就是要認證 認證制度是3次 postback 因為會暫存也被丟過來"""
    role = get_pending_role(user_id)
    if verify_password(role, text):
        save_user_role(user_id, role)
        complete_auth(user_id)
        msg = f"密碼正確，您已成功認證為：{ROLE_TEXT_MAP.get(role, role)}"
    else:
        attempts = increment_attempt(user_id)
        if attempts >= 3:
            complete_auth(user_id)
            msg = "❌ 已連續輸入錯誤 3 次，已幫您轉換為QA回答模式。若想請重新驗證請選擇角色。"
        else:
            remaining = 3 - attempts
            msg = f"❌ 密碼錯誤，請重新輸入。您還有 {remaining} 次機會"

    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=msg)]
        )
    )


def handle_rag_flow(text, user_id, index, namespace, line_bot_api, event):
    """取得mongo user role 進行RAG"""
    user = get_user_role(user_id)
    if user:
        try:
            rag_answer = answer_query_secure(text, user_id, index, namespace)
        except Exception as e:
            print("❌ RAG 查詢失敗：", str(e))
            rag_answer = "❌ 回答時發生錯誤，請稍後再試。"
    else:
        rag_answer = "⚠️ 查無使用者身份資訊，請先完成認證。"

    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=rag_answer)]
        )
    )


def verify_password(role: str, password: str) -> bool:
    """驗證密碼"""
    import os
    expected = os.getenv(f"PASSWORD_{role.upper()}")
    return password == expected


if __name__ == "__main__":

    # poetry run python -m line_bot.handlers.message 

    import os
    from unittest.mock import MagicMock
    from linebot.v3.webhooks.models import MessageEvent

    # ✅ 設定環境變數：密碼 admin 對應的密碼為 1234
    os.environ["PASSWORD_ADMIN"] = "1234"

    # ✅ 建立假的 LINE Messaging API（不真的呼叫 LINE）
    class MockLineAPI:
        def reply_message(self, request):
            print(f"[🧪 MOCK REPLY] {request.reply_token}: {[m.text for m in request.messages]}")

    # ✅ 替換 get_line_api 成為 mock（這一步要在 import handle_message 之前）
    from config import environment
    environment.get_line_api = lambda: MockLineAPI()

    # ✅ 最後再 import handle_message，確保用到的是 mock 過的版本
    from line_bot.handlers.message import handle_message

    # ✅ 第 1 筆訊息：模擬「認證：admin」
    json_event_1 = {
    "replyToken": "token_1",
    "type": "message",
    "mode": "active",
    "timestamp": 1716890993000,
    "webhookEventId": "mock_event_id_1",  # ✅ 加上這個
    "deliveryContext": {"isRedelivery": False},  # ✅ 加上這個
    "source": {
        "type": "user",
        "userId": "U1234567890"
    },
    "message": {
        "type": "text",
        "id": "msg_1",
        "text": "認證：admin",
        "quoteToken": "qt_1",
        "emojis": [],
        "mention": {"mentionees": []}
    }
}


    # ✅ 第 2 筆訊息：模擬「輸入正確密碼」
    json_event_2 = {
    "replyToken": "token_2",
    "type": "message",
    "mode": "active",
    "timestamp": 1716890993000,
    "webhookEventId": "mock_event_id_2",  # ✅ 加上這個
    "deliveryContext": {"isRedelivery": False},  # ✅ 加上這個
    "source": {
        "type": "user",
        "userId": "U1234567890"
    },
    "message": {
        "type": "text",
        "id": "msg_1",
        "text": "認證：admin",
        "quoteToken": "qt_1",
        "emojis": [],
        "mention": {"mentionees": []}
    }
}


    # ✅ 執行身份認證的完整兩步
    print("\n--- 🔐 Step 1：送出 認證：admin ---")
    handle_message(MessageEvent.from_dict(json_event_1))

    print("\n--- 🔐 Step 2：送出 密碼 1234 ---")
    handle_message(MessageEvent.from_dict(json_event_2))
