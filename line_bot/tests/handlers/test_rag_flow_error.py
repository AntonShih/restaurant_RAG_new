# 測message中handle_message 第二邏輯handle_rag_flow使用者為認證 = none
# 則返回⚠️ 查無使用者身份資訊

# 測試指令 全域 $env:PYTHONPATH="."; poetry run pytest
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers/test_rag_flow_error.py -s


# def test_rag_query_unauthenticated_user(monkeypatch):
#     from line_bot.services import user_service
#     monkeypatch.setattr(user_service, "get_user_role", lambda user_id: None)

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
#         "replyToken": "token_fail",
#         "type": "message",
#         "mode": "active",
#         "timestamp": 1716890993000,
#         "webhookEventId": "mock_event_rag",
#         "deliveryContext": {"isRedelivery": False},
#         "source": {"type": "user", "userId": "U000000"},
#         "message": {"type": "text", "id": "msg1", "quoteToken": "qt_2","text": "查詢：關店流程"}
#     }

#     handle_message(MessageEvent.from_dict(json_event), line_bot_api, "mock_index", "mock-namespace")
#     assert "⚠️ 查無使用者身份資訊" in line_bot_api.replies[-1][0]

def test_rag_query_unauthenticated_user(monkeypatch, mock_line_api, mock_no_user):
    from line_bot.handlers.message import handle_message
    from linebot.v3.webhooks.models import MessageEvent

    json_event = {
        "replyToken": "token_fail",
        "type": "message",
        "mode": "active",
        "timestamp": 1716890993000,
        "webhookEventId": "mock_event_rag",
        "deliveryContext": {"isRedelivery": False},
        "source": {"type": "user", "userId": "U000000"},
        "message": {"type": "text", "id": "msg1", "quoteToken": "qt_2","text": "查詢：關店流程"}
    }

    handle_message(MessageEvent.from_dict(json_event), mock_line_api, "mock_index", "mock-namespace")
    assert "⚠️ 查無使用者身份資訊" in mock_line_api.replies[-1][0]


