
from linebot.v3.webhooks import PostbackEvent
from services.postback_service import PostbackService

def handle_postback(event: PostbackEvent, line_bot_api):
    """
    Postback 事件接收點，負責轉交至 Service 層處理。
    """
    user_id = event.source.user_id
    data = event.postback.data

    PostbackService(user_id, data, line_bot_api, event).process()
