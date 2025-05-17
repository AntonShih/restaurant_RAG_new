from linebot.v3.webhooks import MessageEvent, PostbackEvent, TextMessageContent
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
import os
from line_bot.models import save_user_role, get_user_role
from RAG.query.query_engine_safe import answer_query_secure


# 初始化 LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)

# 身分認證暫存區（可選：改成 Redis）
pending_password_check = {}  # user_id: role（等待輸入密碼）

# 🌟 身分名稱對照表
role_text_map = {
    "normal": "一般職員",
    "reserve": "儲備幹部",
    "leader": "組長",
    "vice_manager": "副店長",
    "manager": "店長"
}

def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        # ✅ 使用者從 Rich Menu 點選了身份（如：認證：kitchen）
        if text.startswith("認證："):
            role = text.replace("認證：", "").strip()
            pending_password_check[user_id] = role

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=f"🔐 請輸入 {role_text_map.get(role, role)} 的密碼")]
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
                        messages=[TextMessage(text=f"✅ 密碼正確，您已成功認證為：{role_text_map.get(role)}")]
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

        # ✅ 啟動 RAG 查詢流程
        response = answer_query_secure(text, user_id)

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response)]
            )
        )


def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data

    if data.startswith("role:"):
        role = data.split(":")[1]
        pending_password_check[user_id] = role

        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=f"🔐 請輸入 {role_text_map.get(role, role)} 的密碼")]
                )
            )
