# 測試指令 全域 $env:PYTHONPATH="."; poetry run pytest
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers/test_identity_flow.py
import pytest
from unittest.mock import MagicMock, patch
from linebot.v3.webhooks import MessageEvent, TextMessageContent, SourceUser
from linebot.v3.messaging import TextMessage

from line_bot.handlers.message import handle_identity_auth_flow
from line_bot.services import auth_state
from line_bot.config.role_config import ROLE_TEXT_MAP

@pytest.fixture
def mock_event():
    return MessageEvent(
        message=TextMessageContent(text="認證：主管"),
        reply_token="dummy_token",
        source=SourceUser(user_id="U_test")
    )

@pytest.fixture
def mock_line_bot_api():
    return MagicMock()

def test_identity_auth_flow_triggers_start(mock_event, mock_line_bot_api):
    with patch.object(auth_state, "start_auth") as mock_start_auth:
        handled = handle_identity_auth_flow(
            text=mock_event.message.text,
            user_id=mock_event.source.user_id,
            line_bot_api=mock_line_bot_api,
            event=mock_event
        )
        assert handled is True
        mock_start_auth.assert_called_once_with("U_test", "主管")
        mock_line_bot_api.reply_message.assert_called_once()
        args, _ = mock_line_bot_api.reply_message.call_args
        reply = args[0].messages[0]
        expected_text = f"🔐 請輸入 {ROLE_TEXT_MAP.get('主管', '主管')} 的密碼"
        assert isinstance(reply, TextMessage)
        assert reply.text == expected_text
