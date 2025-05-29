# 測 handle_message handle_rag_flow 中有認證但rag壞掉的狀況

# 測試指令 全域 $env:PYTHONPATH="."; poetry run pytest
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers/
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers/test_rag_with_auth_but_fail.py

# def test_rag_query_exception_handling(monkeypatch):
#     from line_bot.services import user_service
#     monkeypatch.setattr(user_service, "get_user_role", lambda user_id: {"user_id": user_id, "role": "admin"})

#     from RAG.query import query_engine_safe
#     def rag爆炸(*args, **kwargs): raise Exception("RAG 爆掉了")
#     monkeypatch.setattr(query_engine_safe, "answer_query_secure", rag爆炸)

#     class MockLineAPI:
#         def __init__(self): self.replies = []
#         def reply_message(self, request):
#             self.replies.append([m.text for m in request.messages])
#     line_bot_api = MockLineAPI()

#     from config import environment
#     monkeypatch.setattr(environment, "get_pinecone_index", lambda: "mock_index")
#     monkeypatch.setattr(environment, "get_namespace", lambda: "mock-namespace")

#     from line_bot.handlers.message import handle_message
#     from linebot.v3.webhooks.models import MessageEvent

#     json_event = {
#         "replyToken": "token_rag_ex",
#         "type": "message",
#         "mode": "active",
#         "timestamp": 1716890993000,
#         "webhookEventId": "mock_event_ex",
#         "deliveryContext": {"isRedelivery": False},
#         "source": {"type": "user", "userId": "user_id"},
#         "message": {"type": "text", "id": "msg1", "quoteToken": "qt_2", "text": "系統異常查詢"}
#     }

#     handle_message(MessageEvent.from_dict(json_event), line_bot_api, "mock_index", "mock-namespace")
#     assert "❌ 回答時發生錯誤" in line_bot_api.replies[-1][0]

# 測 handle_message handle_rag_flow 中有認證但 rag 爆掉的狀況

def test_rag_query_exception_handling(monkeypatch, mock_line_api, mock_admin):
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
        "source": {"type": "user", "userId": "user_id"},
        "message": {
            "type": "text",
            "id": "msg1",
            "quoteToken": "qt_2",
            "text": "系統異常查詢"
        }
    }

    handle_message(MessageEvent.from_dict(json_event), mock_line_api, "mock_index", "mock-namespace")
    assert "❌ 回答時發生錯誤" in mock_line_api.replies[-1][0]
