from linebot.v3.webhooks import MessageEvent, PostbackEvent, TextMessageContent
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
import os
from line_bot.models import save_user_role, get_user_role

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

        # ✅ 一般訊息根據身份回覆對應內容，抓腳色
        user_doc = get_user_role(user_id)
        role = user_doc["role"] if user_doc else "guest"

        reply = {
            "normal": "🍳 一般職員，請檢查備料清單並確認溫控紀錄。",
            "reserve": "🧑‍🎓 儲備幹部，今日任務請至公告欄查看。",
            "leader": "👩‍🔧 組長您好，請確認排班表並檢查員工出勤。",
            "vice_manager": "👨‍💼 副店長，協助店長處理營運狀況。",
            "manager": "👑 店長您好，這是您的營運報表與 SOP：...",
            "guest": "請先輸入「認證」以選擇您的職等"
        }.get(role, "請先認證")

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply)]
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
