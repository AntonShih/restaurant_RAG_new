import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Header, HTTPException
from contextlib import asynccontextmanager
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent

from line_bot.db.mongodb import get_db, close_mongodb_client
from line_bot.services.user_service import init_user_roles_index
from line_bot.handlers.message import handle_message
from line_bot.handlers.postback import handle_postback

load_dotenv()
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_db()
    init_user_roles_index()
    print(f"✅ MongoDB 已啟動，資料庫名稱：{db.name}")
    yield
    close_mongodb_client()
    print("🛑 MongoDB 已關閉")

app = FastAPI(lifespan=lifespan)

# 加入事件處理器
@handler.add(MessageEvent, message=TextMessageContent)
def _handle_message(event):
    print("🎯 _handle_message 被呼叫了！")
    handle_message(event)

@handler.add(PostbackEvent)
def _handle_postback(event):
    print("🎯 _handle_postback 被呼叫了！")
    handle_postback(event)

# Webhook 路由
@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(...)):
    body = await request.body()
    body_str = body.decode("utf-8")

    try:
        handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return {"status": "ok"}
# ----------------------------------------------------------------------------------------------
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from dotenv import load_dotenv
# from fastapi import FastAPI, Request, Header, HTTPException
# from contextlib import asynccontextmanager
# from linebot.v3 import WebhookHandler
# from linebot.v3.exceptions import InvalidSignatureError
# from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent

# from line_bot.db.mongodb import get_db, close_mongodb_client
# from line_bot.services.user_service import init_user_roles_index
# from line_bot.handlers.message import handle_message
# from line_bot.handlers.postback import handle_postback
# from traceback import format_exc

# load_dotenv()
# handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
# print("✅ LINE_CHANNEL_SECRET =", os.getenv("LINE_CHANNEL_SECRET"))


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     db = get_db()
#     await init_user_roles_index()
#     print(f"✅ MongoDB 已啟動，資料庫名稱：{db.name}")
#     yield
#     close_mongodb_client()
#     print("🛑 MongoDB 已關閉")

# app = FastAPI(lifespan=lifespan)

# @handler.add(MessageEvent, message=TextMessageContent)
# async def on_message(event):
#     print("🎯 _handle_message 被呼叫了！")
#     await handle_message(event)

# @handler.add(PostbackEvent)
# async def on_postback(event):
#     print("🎯 _handle_postback 被呼叫了！")
#     await handle_postback(event)

# @app.post("/callback")
# async def callback(request: Request, x_line_signature: str = Header(None)):
#     print("📩 收到 LINE Webhook")
#     try:
#         body = await request.body()
#         body_str = body.decode("utf-8")
#         print("🔎 Webhook Raw:\n", body_str)
#         print("🔑 X-Line-Signature:\n", x_line_signature)

#         await handler.handle_async(body_str, x_line_signature)
#         print("✅ handle_async 執行完成")

#     except InvalidSignatureError:
#         print("❌ 簽名驗證失敗")
#         raise HTTPException(status_code=400, detail="Invalid signature")

#     except Exception:
#         print("❌ Uncaught Exception：")
#         print(format_exc())
#         raise HTTPException(status_code=500, detail="Internal Server Error")

#     return {"status": "ok"}

# print("✅ WebhookHandler 來源：", WebhookHandler.__module__)
# import inspect
# print("📍 WebhookHandler 定義位置：", inspect.getfile(WebhookHandler))

# from linebot.v3.webhook import WebhookHandler
# print("✅ handle_async 存在嗎？", hasattr(WebhookHandler, "handle_async"))


# @handler.default()
# async def fallback(event):
#     print("⚠️ 未被任何 handler 捕捉到的事件：", event)
# -------------------------------------------------------------
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from dotenv import load_dotenv
# from fastapi import FastAPI, Request, Header, HTTPException
# from contextlib import asynccontextmanager
# from linebot.v3 import WebhookHandler
# from linebot.v3.exceptions import InvalidSignatureError
# from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent

# from line_bot.db.mongodb import get_db, close_mongodb_client
# from line_bot.services.user_service import init_user_roles_index
# from line_bot.handlers.message import handle_message
# from line_bot.handlers.postback import handle_postback

# load_dotenv()
# handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     db = get_db()
#     init_user_roles_index()
#     print(f"✅ MongoDB 已啟動，資料庫名稱：{db.name}")
#     yield
#     close_mongodb_client()
#     print("🛑 MongoDB 已關閉")

# app = FastAPI(lifespan=lifespan)

# # 加入事件處理器
# @handler.add(MessageEvent, message=TextMessageContent)
# def _handle_message(event):
#     print("🎯 _handle_message 被呼叫了！")
#     handle_message(event)

# @handler.add(PostbackEvent)
# def _handle_postback(event):
#     print("🎯 _handle_postback 被呼叫了！")
#     handle_postback(event)

# # Webhook 路由
# @app.post("/callback")
# async def callback(request: Request, x_line_signature: str = Header(...)):
#     body = await request.body()
#     body_str = body.decode("utf-8")

#     try:
#         handler.handle(body_str, x_line_signature)
#     except InvalidSignatureError:
#         raise HTTPException(status_code=400, detail="Invalid signature")

#     return {"status": "ok"}
