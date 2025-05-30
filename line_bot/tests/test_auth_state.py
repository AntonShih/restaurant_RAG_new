# 測試魔咒 :  $env:PYTHONPATH = Get-Location
# pytest RAG/tests/

from line_bot.services import auth_state


def test_start_auth():
    user_id = "U123456"
    role = "店長"
    auth_state.start_auth(user_id, role)
    assert user_id in auth_state.pending_password_check
    assert auth_state.pending_password_check[user_id]["role"] == role
    assert auth_state.pending_password_check[user_id]["attempts"] == 0


def test_complete_auth():
    user_id = "U123456"
    auth_state.pending_password_check[user_id] = {"role": "店長", "attempts": 0}
    auth_state.complete_auth(user_id)
    assert user_id not in auth_state.pending_password_check


def test_is_auth_pending_true():
    user_id = "U123456"
    auth_state.pending_password_check[user_id] = {"role": "店長", "attempts": 0}
    assert auth_state.is_auth_pending(user_id) is True


def test_is_auth_pending_false():
    user_id = "U654321"
    assert auth_state.is_auth_pending(user_id) is False


def test_get_pending_role():
    user_id = "U123456"
    auth_state.pending_password_check[user_id] = {"role": "副店長", "attempts": 0}
    assert auth_state.get_pending_role(user_id) == "副店長"


def test_get_pending_role_none():
    user_id = "U000000"
    assert auth_state.get_pending_role(user_id) is None


def test_increment_attempt():
    user_id = "U123456"
    auth_state.pending_password_check[user_id] = {"role": "店長", "attempts": 0}
    count = auth_state.increment_attempt(user_id)
    assert count == 1
    assert auth_state.pending_password_check[user_id]["attempts"] == 1


def test_increment_attempt_unknown_user():
    user_id = "U999999"
    count = auth_state.increment_attempt(user_id)
    assert count == 0
