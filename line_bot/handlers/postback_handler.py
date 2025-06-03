# 接post back的地方
from linebot.v3.messaging import ReplyMessageRequest
from services.postback_service import PostbackService


def handle_postback(event, line_bot_api):
    user_id = event.source.user_id
    data = event.postback.data

    message = PostbackService(user_id, data).process()

    if message:
        #  LINE v3 正確回覆方式（用 ReplyMessageRequest 包起來）
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[message]  #  一定要是 list
            )
        )

