# 測 verify_password

# 測試指令 全域 $env:PYTHONPATH="."; poetry run pytest
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers
# $env:PYTHONPATH="." ; poetry run pytest line_bot/tests/handlers/test_verify_password.py
from line_bot.handlers.message import verify_password

def test_verify_password(monkeypatch):
    monkeypatch.setenv("PASSWORD_MANAGER", "1234")
    assert verify_password("manager", "1234") is True
    assert verify_password("manager", "wrong") is False


