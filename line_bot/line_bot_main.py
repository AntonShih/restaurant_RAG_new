from fastapi import FastAPI, Request, Header, HTTPException
from contextlib import asynccontextmanager
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent

from line_bot.db.mongodb import get_db, close_mongodb_client
from line_bot.services.user_service import init_user_roles_index
from line_bot.handlers.message import handle_message
from line_bot.handlers.postback import handle_postback
from config.environment import init_openai, init_pinecone, get_pinecone_index, get_namespace,get_line_handler,get_line_api

init_openai()
init_pinecone()
INDEX = get_pinecone_index()
NAMESPACE = get_namespace()
handler = get_line_handler()
line_bot_api = get_line_api()


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
    handle_message(event, line_bot_api, INDEX, NAMESPACE)

@handler.add(PostbackEvent)
def _handle_postback(event):
    print("🎯 _handle_postback 被呼叫了！")
    handle_postback(event, line_bot_api)

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
