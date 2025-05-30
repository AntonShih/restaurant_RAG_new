# 測試 handle_message 認證錯三次會不會被攔截，切回查詢
# 先將user 假裝輸入認證:進入驗證邏輯存在暫存
# 刻意輸入錯四次密碼
# 比對assert是否相同 ❌ 已連續輸入錯誤 3 次，已幫您轉換為QA回答模式。若想請重新驗證請選擇角色。"

# 測試指令 全域 $env:PYTHONPATH="."; poetry run pytest
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers/test_auth_flow.py

from linebot.v3.webhooks.models import MessageEvent
from line_bot.handlers.message import handle_message

def test_auth_fail_three_times(mock_line_api):

    # ✅ 第一筆訊息：模擬「認證：admin」
    json_event_1 = {
        "replyToken": "token_1",
        "type": "message",
        "mode": "active",
        "timestamp": 1716890993000,
        "webhookEventId": "mock_event_id_1",
        "deliveryContext": {"isRedelivery": False},
        "source": {"type": "user", "userId": "U1234567890"},
        "message": {"type": "text", "id": "msg_1", "quoteToken": "qt_1", "text": "認證：admin"}
    }

    # ✅ 三次錯誤密碼的事件模板
    def json_wrong_pw(token):
        return {
            "replyToken": token,
            "type": "message",
            "mode": "active",
            "timestamp": 1716890993000,
            "webhookEventId": f"mock_event_fail_{token}",
            "deliveryContext": {"isRedelivery": False},
            "source": {"type": "user", "userId": "U1234567890"},
            "message": {"type": "text", "id": "msg_fail", "quoteToken": "qt_2", "text": "錯的密碼"}
        }

    # ✅ 執行驗證流程
    handle_message(MessageEvent.from_dict(json_event_1), mock_line_api, "mock_index", "mock-namespace")
    handle_message(MessageEvent.from_dict(json_wrong_pw("t1")), mock_line_api, "mock_index", "mock-namespace")
    handle_message(MessageEvent.from_dict(json_wrong_pw("t2")), mock_line_api, "mock_index", "mock-namespace")
    handle_message(MessageEvent.from_dict(json_wrong_pw("t3")), mock_line_api, "mock_index", "mock-namespace")

    # ✅ 結果比對
    assert "🔐 請輸入 admin 的密碼" in mock_line_api.replies[0][0]
    assert "❌ 密碼錯誤，請重新輸入。您還有 2 次機會" in mock_line_api.replies[1][0]
    assert "❌ 密碼錯誤，請重新輸入。您還有 1 次機會" in mock_line_api.replies[2][0]
    assert "❌ 已連續輸入錯誤 3 次，已幫您轉換為QA回答模式。若想請重新驗證請選擇角色。" in mock_line_api.replies[3][0]
