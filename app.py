from fastapi import FastAPI, Request, Header, HTTPException
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from dotenv import load_dotenv
import os

# ⬇️ 引入剛剛寫好的模組
from linebot_webhook_handler import handle_message, handle_postback
from linebot_webhook_handler import router as liff_router

load_dotenv()
app = FastAPI()
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(...)):
    body = await request.body()
    body_str = body.decode("utf-8")
    try:
        handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return {"status": "ok"}

# 綁定事件
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent

@handler.add(MessageEvent, message=TextMessageContent)
def _handle_message(event):
    handle_message(event)

@handler.add(PostbackEvent)
def _handle_postback(event):
    handle_postback(event)


app.include_router(liff_router)
