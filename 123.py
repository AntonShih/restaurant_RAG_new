from fastapi import FastAPI, Request, Header, HTTPException
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, TemplateMessage,
    ButtonsTemplate, PostbackAction
)
from linebot.v3.webhooks import MessageEvent, PostbackEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError
from dotenv import load_dotenv
import os
from linebot.v3.messaging import CarouselTemplate, CarouselColumn


load_dotenv()  # 載入 .env

app = FastAPI()

# 初始化 LINE Bot
configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 記憶體模擬身份儲存（正式請改 DB）
user_roles = {}  # user_id: role

pending_password_check = {}  # user_id: role（等待輸入哪個職位的密碼）


@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(...)):
    body = await request.body()
    body_str = body.decode("utf-8")
    try:
        handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return {"status": "ok"}

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        # 若使用者正在進行密碼認證
        if user_id in pending_password_check:
            role = pending_password_check[user_id]
            expected_password = os.getenv(f"PASSWORD_{role.upper()}")  # 取對應密碼

            if text == expected_password:
                user_roles[user_id] = role
                del pending_password_check[user_id]
                role_name = {
                    "kitchen": "內場人員",
                    "front": "外場人員",
                    "reserve": "儲備幹部",
                    "leader": "組長",
                    "vice_manager": "副店長",
                    "manager": "店長"
                }[role]
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=f"✅ 密碼正確，您已成功認證為：{role_name}")]
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

        # 使用者輸入認證
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

        else:
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


@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data

    if data.startswith("role:"):
        role = data.split(":")[1]
        pending_password_check[user_id] = role  # 儲存要驗證哪個角色密碼

        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            role_text = {
                "kitchen": "內場人員",
                "front": "外場人員",
                "reserve": "儲備幹部",
                "leader": "組長",
                "vice_manager": "副店長",
                "manager": "店長"
            }
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=f"🔐 請輸入 {role_text.get(role, '該職等')} 的密碼")]
                )
            )
