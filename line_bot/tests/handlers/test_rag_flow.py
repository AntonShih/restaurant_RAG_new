# 測試指令 全域 $env:PYTHONPATH="."; poetry run pytest
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers/test_rag_flow.py -s



import os
import pytest
from linebot.v3.webhooks.models import MessageEvent
from config import environment
from line_bot.handlers.message import handle_message

class MockLineAPI:
    def reply_message(self, request):
        print(f"[🧪 MOCK REPLY] {request.reply_token}: {[m.text for m in request.messages]}")

@pytest.fixture(autouse=True)
def setup_mock(monkeypatch):
    os.environ["PASSWORD_ADMIN"] = "1234"
    monkeypatch.setattr(environment, "get_line_api", lambda: MockLineAPI())

def build_mock_event(reply_token, user_id, text, msg_id="mock_msg"):
    return MessageEvent.from_dict({
        "replyToken": reply_token,
        "type": "message",
        "mode": "active",
        "timestamp": 1716890993000,
        "webhookEventId": "mock_event_id",
        "deliveryContext": {"isRedelivery": False},
        "source": {"type": "user", "userId": user_id},
        "message": {
            "type": "text",
            "id": msg_id,
            "text": text,
            "quoteToken": "qt",
            "emojis": [],
            "mention": {"mentionees": []}
        }
    })

def test_identity_auth_flow():
    user_id = "U1234567890"

    print("\n--- 🔐 Step 1：送出 認證：admin ---")
    event1 = build_mock_event("token_1", user_id, "認證：admin")
    handle_message(event1)

    print("\n--- 🔐 Step 2：送出 密碼 1234 ---")
    event2 = build_mock_event("token_2", user_id, "1234")
    handle_message(event2)
