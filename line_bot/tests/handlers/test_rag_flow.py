# 測試單筆資訊進入handle_message 使用者不在暫存名單(也就是單純查詢)
# 應該執行 取得mongo user role 進行RAG
# 此將api mongo user 預設假帳號{"user_id": user_id, "role": "admin"}
# RAG mock 預設返回 "這是假的答案"

# 測試指令 全域 $env:PYTHONPATH="."; poetry run pytest
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers/test_rag_flow.py -s


# import os
# from linebot.v3.webhooks.models import MessageEvent


# def test_rag_query_with_authenticated_user(monkeypatch):
#     os.environ["PASSWORD_ADMIN"] = "1234"

#     class MockLineAPI:
#         def __init__(self):
#             self.replies = []
#         def reply_message(self, request):
#             self.replies.append([m.text for m in request.messages])

#     line_bot_api = MockLineAPI()

#     from config import environment
#     monkeypatch.setattr(environment, "get_line_api", lambda: line_bot_api)
#     monkeypatch.setattr(environment, "get_pinecone_index", lambda: "mock_index")
#     monkeypatch.setattr(environment, "get_namespace", lambda: "mock-namespace")

#     # ✅ mock 掉 get_user_role：假裝這個人已經登入成功
#     from line_bot.services import user_service
#     monkeypatch.setattr(user_service, "get_user_role", lambda user_id: {"user_id": user_id, "role": "admin"})

#     # ✅ mock 掉 answer_query_secure：避免真的查向量
#     from RAG.query import query_engine_safe
#     monkeypatch.setattr(query_engine_safe, "answer_query_secure", lambda q, u, i, n: "這是假的答案")

#     from linebot.v3.webhooks.models import MessageEvent
#     from line_bot.handlers.message import handle_message

#     # ✅ 傳入問題
#     json_event = {
#         "replyToken": "token_rag",
#         "type": "message",
#         "mode": "active",
#         "timestamp": 1716890993000,
#         "webhookEventId": "mock_event_rag",
#         "deliveryContext": {"isRedelivery": False},
#         "source": {"type": "user", "userId": "U999999"},
#         "message": {
#             "type": "text",
#             "id": "msg_rag",
#             "quoteToken": "qt_2",
#             "text": "請問關店流程？"
#         }
#     }

#     handle_message(MessageEvent.from_dict(json_event), line_bot_api, "mock_index", "mock-namespace")

#     assert "這是假的答案" in line_bot_api.replies[-1]

def test_rag_query_with_authenticated_user(monkeypatch, mock_line_api, mock_admin):
    from RAG.query import query_engine_safe
    monkeypatch.setattr(query_engine_safe, "answer_query_secure", lambda q, u, i, n: "這是假的答案")

    from linebot.v3.webhooks.models import MessageEvent
    from line_bot.handlers.message import handle_message

    json_event = {
        "replyToken": "token_rag",
        "type": "message",
        "mode": "active",
        "timestamp": 1716890993000,
        "webhookEventId": "mock_event_rag",
        "deliveryContext": {"isRedelivery": False},
        "source": {"type": "user", "userId": "U999999"},
        "message": {
            "type": "text",
            "id": "msg_rag",
            "quoteToken": "qt_2",
            "text": "請問關店流程？"
        }
    }

    handle_message(MessageEvent.from_dict(json_event), mock_line_api, "mock_index", "mock-namespace")
    assert "這是假的答案" in mock_line_api.replies[-1]
