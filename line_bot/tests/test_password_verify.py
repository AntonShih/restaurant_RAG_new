import pytest
from line_bot.handlers.message import verify_password

def test_verify_password_correct(monkeypatch):
    monkeypatch.setenv("PASSWORD_店長", "1357")
    assert verify_password("店長", "1357") is True

def test_verify_password_incorrect(monkeypatch):
    monkeypatch.setenv("PASSWORD_店長", "1357")
    assert verify_password("店長", "0000") is False

def test_verify_password_missing(monkeypatch):
    monkeypatch.delenv("PASSWORD_副店長", raising=False)
    assert verify_password("副店長", "1234") is False
