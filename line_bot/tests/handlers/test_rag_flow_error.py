# 測message中handle_message 第二邏輯handle_rag_flow使用者為認證 = none
# 則返回⚠️ 查無使用者身份資訊

# 測試指令 全域 $env:PYTHONPATH="."; poetry run pytest
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers/test_rag_flow_error.py -s


def test_rag_query_unauthenticated_user(monkeypatch, mock_line_api):
    monkeypatch.setattr("line_bot.handlers.message.get_user_role", lambda user_id: None)

    from line_bot.handlers.message import handle_message
    from linebot.v3.webhooks.models import MessageEvent

    
    json_event = {
        "replyToken": "token_fail",
        "type": "message",
        "mode": "active",
        "timestamp": 1716890993000,
        "webhookEventId": "mock_event_rag",
        "deliveryContext": {"isRedelivery": False},
        "source": {"type": "user", "userId": "U1234567890"},
        "message": {"type": "text", "id": "msg1", "quoteToken": "qt_2","text": "查詢：關店流程"}
    }

    handle_message(MessageEvent.from_dict(json_event), mock_line_api, "mock_index", "mock-namespace")
    assert "⚠️ 查無使用者身份資訊" in mock_line_api.replies[-1][0]


