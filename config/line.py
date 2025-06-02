import os
from dotenv import load_dotenv
from linebot.v3.messaging import Configuration, MessagingApi, ApiClient
from linebot.v3 import WebhookHandler

load_dotenv()

def get_line_configuration():
    """取得 LINE SDK 所需的設定物件"""
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    return Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)

# def get_line_api() -> MessagingApi:
#     """return MessagingApi(client)"""
#     config = get_line_configuration()
#     client = ApiClient(config)
#     return MessagingApi(client)

def get_line_handler() -> WebhookHandler:
    """取得 WebhookHandler 實例"""
    LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    return WebhookHandler(LINE_CHANNEL_SECRET)