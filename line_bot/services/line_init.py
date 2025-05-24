# # 用來集中管理 LINE Bot 的 Messaging API 與 Webhook 驗證元件
# # ✅ 同步版初始化

# import os
# from dotenv import load_dotenv
# from linebot.v3.messaging import Configuration, ApiClient, MessagingApi
# from linebot.v3.webhook import WebhookParser

# load_dotenv()

# LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
# LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

# # 初始化 Configuration 與 MessagingApi
# configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
# api_client = ApiClient(configuration)
# line_bot_api = MessagingApi(api_client)

# # 用來驗證 webhook 簽名（如果你有用）
# parser = WebhookParser(LINE_CHANNEL_SECRET)

# print("✅ LINE Bot 同步 API 初始化完成")

# __all__ = ["line_bot_api", "parser"]

# # -------------------------------------------------------------------
# async 版本

# import os
# from dotenv import load_dotenv
# from linebot.v3.messaging import Configuration, AsyncApiClient, AsyncMessagingApi
# from linebot.v3.webhook import WebhookParser

# load_dotenv()

# # 從 .env 讀取 LINE 開發者後台的金鑰
# LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
# LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

# # 初始化 LINE Messaging API（你之後用來回訊息的對象）
# configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
# async_api_client = AsyncApiClient(configuration)
# line_bot_api = AsyncMessagingApi(async_api_client)

# # 初始化用來驗證簽名的 parser（選用：如果你手動 parse webhook）
# parser = WebhookParser(LINE_CHANNEL_SECRET)

# print("✅ LINE Bot API 與 WebhookParser 初始化完成")

# __all__ = ["line_bot_api", "parser"]