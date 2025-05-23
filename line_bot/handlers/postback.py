
from linebot.v3.webhooks import PostbackEvent
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
import os

from line_bot.config.role_config import ROLE_TEXT_MAP
from line_bot.services.auth_state import start_auth  # ✅ 用封裝好的

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)

def handle_postback(event: PostbackEvent):
    user_id = event.source.user_id
    data = event.postback.data

    if data.startswith("role:"):
        role = data.split(":")[1]
        start_auth(user_id, role)  # ✅ 統一入口

        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        TextMessage(
                            text=f"🔐 請輸入 {ROLE_TEXT_MAP.get(role, role)} 的密碼")
                    ]
                )
            )
# -----------------------------------------------------------------------------------
# from linebot.v3.webhooks import PostbackEvent
# from linebot.v3.messaging import (
#     Configuration, ApiClient, MessagingApi,
#     ReplyMessageRequest, TextMessage
# )
# import os

# from line_bot.config.role_config import ROLE_TEXT_MAP
# from line_bot.services.auth_state import start_auth  # ✅ 用封裝好的

# LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
# configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
# line_api = MessagingApi(ApiClient(configuration))

# async def handle_postback(event: PostbackEvent):
#     print("🔥 postback 被呼叫了")
#     user_id = event.source.user_id
#     data = event.postback.data

#     if data.startswith("role:"):
#         role = data.split(":")[1]
#         start_auth(user_id, role)

#         await line_api.reply_message(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[
#                     TextMessage(
#                         text=f"🔐 請輸入 {ROLE_TEXT_MAP.get(role, role)} 的密碼"
#                     )
#                 ]
#             )
#         )
