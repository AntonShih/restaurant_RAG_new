# 測試單筆資訊進入handle_message 使用者不在暫存名單(也就是單純查詢)
# 應該執行 取得mongo user role 進行RAG
# 此將api mongo user 預設假帳號{"user_id": user_id, "role": "admin"}
# RAG mock 預設返回 "這是假的答案"

# 測試指令 全域 $env:PYTHONPATH="."; poetry run pytest
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers/test_rag_flow.py -s

# ---------------------------------------------------------------
def test_rag_query_with_authenticated_user(monkeypatch, mock_line_api):
    # 要用 string path monkeypatch 掉模組內部 import 的版本
    monkeypatch.setattr("line_bot.handlers.message.get_user_role", lambda user_id: {
        "user_id": "U123456789",
        "role": "manager",
        "access_level": 5,
    })

    monkeypatch.setattr("line_bot.handlers.message.answer_query_secure", lambda q, u, i, n: "這是假的答案")

    from linebot.v3.webhooks.models import MessageEvent
    from line_bot.handlers.message import handle_message

    json_event = {
        "replyToken": "token_rag",
        "type": "message",
        "mode": "active",
        "timestamp": 1716890993000,
        "webhookEventId": "mock_event_rag",
        "deliveryContext": {"isRedelivery": False},
        "source": {"type": "user", "userId": "U123456789"},
        "message": {
            "type": "text",
            "id": "msg_rag",
            "quoteToken": "qt_2",
            "text": "請問關店流程？"
        }
    }

    handle_message(MessageEvent.from_dict(json_event), mock_line_api, "mock_index", "mock-namespace")
    assert "這是假的答案" in mock_line_api.replies[-1]
