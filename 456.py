from linebot.v3.webhooks import MessageEvent, PostbackEvent, TextMessageContent
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, TemplateMessage,
    ButtonsTemplate, PostbackAction, CarouselTemplate, CarouselColumn
)
import os

# 初始化 LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)

# 身分認證暫存區
user_roles = {}  # user_id: role
pending_password_check = {}  # user_id: role（等待輸入密碼）

# 🌟 身分名稱對照表
role_text_map = {
    "kitchen": "內場人員",
    "front": "外場人員",
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
                user_roles[user_id] = role
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

        # ✅ 使用者輸入「認證」 → 回傳 Carousel 選單
        if text == "認證":
            carousel_template = TemplateMessage(
                alt_text="職等認證選單",
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            title="請選擇您的職等",
                            text="第一頁",
                            actions=[
                                PostbackAction(label="內場人員", data="role:kitchen"),
                                PostbackAction(label="外場人員", data="role:front"),
                                PostbackAction(label="儲備幹部", data="role:reserve")
                            ]
                        ),
                        CarouselColumn(
                            title="請選擇您的職等",
                            text="第二頁",
                            actions=[
                                PostbackAction(label="組長", data="role:leader"),
                                PostbackAction(label="副店長", data="role:vice_manager"),
                                PostbackAction(label="店長", data="role:manager")
                            ]
                        )
                    ]
                )
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[carousel_template]
                )
            )
            return

        # ✅ 一般訊息根據身份回覆對應內容
        role = user_roles.get(user_id, "guest")
        reply = {
            "kitchen": "🍳 內場人員，請檢查備料清單並確認溫控紀錄。",
            "front": "🍽 外場人員，今天的招呼語是：歡迎光臨，我們有新品推薦！",
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
