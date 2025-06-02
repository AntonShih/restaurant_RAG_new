# uvicorn line_bot_main:app --reload

from fastapi import FastAPI, Request, Header, HTTPException
from contextlib import asynccontextmanager
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent

from config.openai import init_openai
from config.pinecone import init_pinecone, get_namespace
from config.line import get_line_handler
from adapters.line_adapter import get_line_api
from adapters.pinecone_adapter import get_pinecone_index
from line_bot1.db.mongodb import get_db, close_mongodb_client
from line_bot1.db.init_db import init_user_roles_index
from line_bot1.handlers.message_handler import handle_message
from line_bot1.handlers.postback_handler import handle_postback
import logging


from config.log_config import init_logging
init_logging(level=logging.DEBUG, to_file=False)


# ✅ 初始化 SDK 與必要變數
init_openai()
init_pinecone()
INDEX = get_pinecone_index()
NAMESPACE = get_namespace()
handler = get_line_handler()
line_bot_api = get_line_api()

# ✅ FastAPI lifespan 設定：啟動與關閉時初始化 MongoDB
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_db()
    init_user_roles_index()
    print(f"✅ MongoDB 已啟動，資料庫名稱：{db.name}")
    yield
    close_mongodb_client()
    print("🛑 MongoDB 已關閉")

app = FastAPI(lifespan=lifespan)

# ✅ LINE Message 事件處理器（文字訊息）
@handler.add(MessageEvent, message=TextMessageContent)
def _handle_message(event):
    print("🎯 收到使用者文字訊息")
    handle_message(event, line_bot_api, INDEX, NAMESPACE)

# ✅ LINE Postback 事件處理器（按鈕點擊）
@handler.add(PostbackEvent)
def _handle_postback(event):
    print("🎯 收到使用者 Postback 資料")
    handle_postback(event, line_bot_api)

# ✅ LINE Webhook callback 路由
@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(...)):
    body = await request.body()
    body_str = body.decode("utf-8")

    try:
        handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return {"status": "ok"}
