
from linebot.v3.webhooks import PostbackEvent
from linebot.v3.messaging import ReplyMessageRequest, TextMessage

from line_bot.config.role_config import ROLE_TEXT_MAP
from line_bot.services.auth_state import start_auth  


def handle_postback(event: PostbackEvent, line_bot_api):
    user_id = event.source.user_id
    data = event.postback.data

    if data.startswith("role:"):
        role = data.split(":")[1]
        start_auth(user_id, role)  # ✅ 統一入口


        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(
                        text=f"🔐 請輸入 {ROLE_TEXT_MAP.get(role, role)} 的密碼")
                ]
            )
        )
