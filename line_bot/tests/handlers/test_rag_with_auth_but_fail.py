# 測 handle_message handle_rag_flow 中有認證但rag壞掉的狀況

# 測試指令 全域 $env:PYTHONPATH="."; poetry run pytest
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers/
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers/test_rag_with_auth_but_fail.py

def test_rag_query_exception_handling(monkeypatch, mock_line_api):

    monkeypatch.setattr("line_bot.handlers.message.get_user_role", lambda user_id: {
        "user_id": "U123456789",
        "role": "manager",
        "access_level": 5,
    })

    from RAG.query import query_engine_safe
    # ❌ 模擬 RAG 內部發生錯誤
    def rag爆炸(*args, **kwargs):
        raise Exception("RAG 爆掉了")
    monkeypatch.setattr(query_engine_safe, "answer_query_secure", rag爆炸)

    from line_bot.handlers.message import handle_message
    from linebot.v3.webhooks.models import MessageEvent

    json_event = {
        "replyToken": "token_rag_ex",
        "type": "message",
        "mode": "active",
        "timestamp": 1716890993000,
        "webhookEventId": "mock_event_ex",
        "deliveryContext": {"isRedelivery": False},
        "source": {"type": "user", "userId": "U123456789"},
        "message": {
            "type": "text",
            "id": "msg1",
            "quoteToken": "qt_2",
            "text": "系統異常查詢"
        }
    }

    handle_message(MessageEvent.from_dict(json_event), mock_line_api, "mock_index", "mock-namespace")
    assert "❌ 回答時發生錯誤" in mock_line_api.replies[-1][0]
