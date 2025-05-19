from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
import os

from line_bot.services.user_service import save_user_role, get_user_role
from line_bot.services.auth_state import pending_password_check
from RAG.query.query_engine_safe import answer_query_secure  # ✅ 改成用 Pinecone + GPT 的流程
from line_bot.config.role_config import ROLE_TEXT_MAP

# 初始化 LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)

def handle_message(event: MessageEvent):
    user_id = event.source.user_id
    text = event.message.text.strip()

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        # ✅ 使用者從 Rich Menu 或純文字輸入了身份（如：認證：reserve）
        if text.startswith("認證："):
            role = text.replace("認證：", "").strip()
            pending_password_check[user_id] = role

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=f"🔐 請輸入 {ROLE_TEXT_MAP.get(role, role)} 的密碼")]
                )
            )
            return

        # ✅ 使用者正在輸入密碼進行認證
        if user_id in pending_password_check:
            role = pending_password_check[user_id]
            expected_password = os.getenv(f"PASSWORD_{role.upper()}")

            if text == expected_password:
                save_user_role(user_id, role)
                del pending_password_check[user_id]
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=f"✅ 密碼正確，您已成功認證為：{ROLE_TEXT_MAP.get(role, role)}")]
                    )
                )
            else:
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text="❌ 密碼錯誤，請重新輸入。")]
                    )
                )
            return

        # ✅ 啟動 RAG 查詢流程（使用 Pinecone + GPT 判斷）
        try:
            response = answer_query_secure(text, user_id)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=str(response).strip())]
                )
            )
        except Exception as e:
            print("❌ GPT 查詢失敗：", str(e))
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="⚠️ 查詢時發生錯誤，請稍後再試。")]
                )
            )
