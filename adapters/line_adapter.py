from config.line import get_line_configuration
from linebot.v3.messaging import MessagingApi, ApiClient

def get_line_api() -> MessagingApi:
    """
    取得 LINE MessagingApi 實例。

    使用 config 中的設定初始化 ApiClient，並回傳可用來發送訊息的 MessagingApi 實例。
    """
    config = get_line_configuration()
    client = ApiClient(config)
    return MessagingApi(client)


def send_reply(line_api: MessagingApi, reply_token: str, message_text: str):
    """
    封裝 LINE Bot 的回覆訊息功能。

    參數:
        line_api (MessagingApi): 已初始化的 LINE Messaging API 實例。
        reply_token (str): 回覆用的 token，由 LINE 傳入事件中提供。
        message_text (str): 要回覆的純文字內容。
    """
    from linebot.v3.messaging import TextMessage, ReplyMessageRequest
    line_api.reply_message(
        ReplyMessageRequest(
            reply_token=reply_token,
            messages=[TextMessage(text=message_text)]
        )
    )
