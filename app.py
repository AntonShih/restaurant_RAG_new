from fastapi import FastAPI, Request, Header, HTTPException
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager

from line_bot.models import init_user_roles_index
from line_bot.mongodb_client import get_db, close_mongodb_client  # ✅ 換成 get_db
from linebot_webhook_handler import handle_message, handle_postback
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent

load_dotenv()
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ 使用 get_db() 正確取得 Database 物件
    db = get_db()
    init_user_roles_index()
    print(f"✅ MongoDB 已啟動，資料庫名稱：{db.name}")
    print("📂 Collections 列表：", db.list_collection_names())
    yield
    close_mongodb_client()
    print("🛑 MongoDB 已關閉")

app = FastAPI(lifespan=lifespan)

@handler.add(MessageEvent, message=TextMessageContent)
def _handle_message(event):
    handle_message(event)

@handler.add(PostbackEvent)
def _handle_postback(event):
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


