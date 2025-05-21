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

from fastapi import FastAPI, Request, Header, HTTPException
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent

from line_bot.db.mongodb import get_db, close_mongodb_client
from line_bot.services.user_service import init_user_roles_index
from line_bot.handlers.message import handle_message
from line_bot.handlers.postback import handle_postback

load_dotenv()

# ✅ 加上啟動前 secret 檢查與保險
line_secret = os.getenv("LINE_CHANNEL_SECRET")
if not line_secret:
    raise RuntimeError("❌ LINE_CHANNEL_SECRET 環境變數未設置")

handler = WebhookHandler(line_secret)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        db = get_db()
        init_user_roles_index()
        print(f"✅ MongoDB 啟動成功，資料庫名稱：{db.name}")
    except Exception as e:
        print(f"❌ lifespan 初始化錯誤：{e}")
    yield
    close_mongodb_client()
    print("🛑 MongoDB 已關閉")

app = FastAPI(lifespan=lifespan)

# ✅ 加上根目錄存活測試
@app.get("/")
def root():
    return {"status": "alive"}

@app.get("/env-check")
def env_check():
    return {
        "LINE_CHANNEL_SECRET": bool(os.getenv("LINE_CHANNEL_SECRET")),
        "MONGODB_URI": bool(os.getenv("MONGODB_URI"))
    }

@handler.add(MessageEvent, message=TextMessageContent)
def _handle_message(event):
    print("🎯 _handle_message 被呼叫了！")
    handle_message(event)

@handler.add(PostbackEvent)
def _handle_postback(event):
    print("🎯 _handle_postback 被呼叫了！")
    handle_postback(event)

@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(...)):
    body = await request.body()
    body_str = body.decode("utf-8")

    try:
        handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return {"status": "ok"}
