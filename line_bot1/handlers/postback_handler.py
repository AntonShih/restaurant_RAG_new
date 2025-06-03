
# from linebot.v3.webhooks import PostbackEvent
# from services.postback_service import PostbackService
# from linebot.models import FlexSendMessage
# from line_bot1.templates.how_to_use import how_to_use_flex

# def handle_postback(event: PostbackEvent, line_bot_api):
#     """
#     Postback 事件接收點，負責轉交至 Service 層處理。
#     """
#     user_id = event.source.user_id
#     data = event.postback.data

#     PostbackService(user_id, data, line_bot_api, event).process()

# # line_bot/handlers/postback_handler.py


# def handle_postback_usage(event, line_bot_api):
#     message = FlexSendMessage(
#         alt_text=how_to_use_flex["altText"],
#         contents=how_to_use_flex["contents"]
#     )
#     line_bot_api.reply_message(event.reply_token, message)

from linebot.v3.messaging import ReplyMessageRequest
from services.postback_service import PostbackService


def handle_postback(event, line_bot_api):
    user_id = event.source.user_id
    data = event.postback.data

    message = PostbackService(user_id, data).process()

    if message:
        # ✅ LINE v3 正確回覆方式（用 ReplyMessageRequest 包起來）
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[message]  # ← 一定要是 list
            )
        )

