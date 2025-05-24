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

# 這邊先用非同步未來好擴展
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
# ------------------------------------------------------------
# -------------------------------------------------------------
# async

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
# from line_bot.services.line_init import line_bot_api  # ✅ 共用 Messaging API 實例

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

# # ✅ async event handler（MessageEvent）
# @handler.add(MessageEvent, message=TextMessageContent)
# async def _handle_message(event: MessageEvent):
#     print("🎯 _handle_message 被呼叫了！")
#     await handle_message(event)

# # ✅ async event handler（PostbackEvent）
# @handler.add(PostbackEvent)
# async def _handle_postback(event: PostbackEvent):
#     print("🎯 _handle_postback 被呼叫了！")
#     await handle_postback(event)

# # ✅ LINE Webhook endpoint
# @app.post("/callback")
# async def callback(request: Request, x_line_signature: str = Header(...)):
#     try:
#         body_bytes = await request.body()
#         body_str = body_bytes.decode("utf-8")
#         await handler.handle_async(body_str, x_line_signature)
#         return {"status": "ok"}
#     except InvalidSignatureError:
#         raise HTTPException(status_code=400, detail="Invalid signature")
#     except Exception as e:
#         print("❌ Webhook 處理錯誤：", str(e))
#         raise HTTPException(status_code=500, detail="Internal Server Error")
