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

