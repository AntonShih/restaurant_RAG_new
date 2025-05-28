# 測試指令 全域 $env:PYTHONPATH="."; poetry run pytest
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers/test_password_flow

from unittest.mock import patch, MagicMock
from linebot.v3.webhooks import MessageEvent, TextMessageContent, SourceUser
from linebot.v3.messaging import TextMessage

from line_bot.handlers.message import handle_pending_password_flow
from line_bot.services import auth_state, user_service

@pytest.fixture
def mock_event():
    return MessageEvent(
        message=TextMessageContent(text="123456"),
        reply_token="dummy_token",
        source=SourceUser(user_id="U_test")
    )

@pytest.fixture
def mock_line_bot_api():
    return MagicMock()

@patch("line_bot.handlers.message.verify_password", return_value=True)
@patch.object(user_service, "save_user_role")
@patch.object(auth_state, "complete_auth")
@patch.object(auth_state, "get_pending_role", return_value="主管")
def test_password_correct(_, __, ___, verify_password, mock_event, mock_line_bot_api):
    handle_pending_password_flow(
        text=mock_event.message.text,
        user_id=mock_event.source.user_id,
        line_bot_api=mock_line_bot_api,
        event=mock_event
    )
    mock_line_bot_api.reply_message.assert_called_once()
    reply = mock_line_bot_api.reply_message.call_args[0][0].messages[0]
    assert isinstance(reply, TextMessage)
    assert "您已成功認證" in reply.text

@patch("line_bot.handlers.message.verify_password", return_value=False)
@patch.object(auth_state, "increment_attempt", return_value=1)
@patch.object(auth_state, "get_pending_role", return_value="主管")
def test_password_wrong_with_retries(_, __, ___, mock_event, mock_line_bot_api):
    handle_pending_password_flow(
        text=mock_event.message.text,
        user_id=mock_event.source.user_id,
        line_bot_api=mock_line_bot_api,
        event=mock_event
    )
    reply = mock_line_bot_api.reply_message.call_args[0][0].messages[0]
    assert "還有" in reply.text and "次機會" in reply.text

@patch("line_bot.handlers.message.verify_password", return_value=False)
@patch.object(auth_state, "increment_attempt", return_value=3)
@patch.object(auth_state, "get_pending_role", return_value="主管")
@patch.object(auth_state, "complete_auth")
def test_password_wrong_exceeded_attempts(_, __, ___, ____, mock_event, mock_line_bot_api):
    handle_pending_password_flow(
        text=mock_event.message.text,
        user_id=mock_event.source.user_id,
        line_bot_api=mock_line_bot_api,
        event=mock_event
    )
    reply = mock_line_bot_api.reply_message.call_args[0][0].messages[0]
    assert "連續輸入錯誤 3 次" in reply.text
